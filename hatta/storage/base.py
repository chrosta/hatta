import datetime
import time
import os, os.path
import mimetypes
import mercurial.simplemerge

from .. import error, page
from werkzeug.urls import url_quote, url_unquote


class StorageError(Exception):
    """Thrown when there are problems with configuration of storage."""


def merge_func(base, other, this):
    """Used for merging edit conflicts."""

    if (base.isbinary() or
        other.isbinary()):
        raise ValueError("can't merge binary data")
    m3 = mercurial.simplemerge.Merge3Text(base.data(), this, other.data())
    return b''.join(m3.merge_lines(start_marker='<<<<<<< local',
                                  mid_marker='=======',
                                  end_marker='>>>>>>> other',
                                  base_marker=None))


class BaseWikiStorage(object):
    """
    Provides means of storing wiki pages and keeping track of their
    change history, using database repository as the storage method.
    """

    def __init__(self, charset=None, _=lambda x: x, unix_eol=False,
                 extension=None, **kwargs):
        """

        """

        self._ = _
        self.charset = charset or 'utf-8'
        self.unix_eol = unix_eol
        self.extension = extension

        self._lastpage = None

    def reopen(self):
        pass

    def __contains__(self, title):
        raise NotImplementedError()

    def open_page(self, title, rev=None, owner='*', meta_only=False):
        """Open the page and return a file-like object with its contents.
        Returns file object, unless meta_only=True, then it returns
        rev, creation_date, owner, comment
        """
        raise NotImplementedError()

    def delete_page(self, title, author, comment, ts=None):
        raise NotImplementedError()

    def repo_revision(self):
        """Give the latest revision of the repository."""
        raise NotImplementedError()

    def page_history(self, title):
        """Iterate over the page's history."""
        raise NotImplementedError()

    def history(self):
        """Iterate over the history of entire wiki.
        path, rev, creation_date, owner, comment
        """
        raise NotImplementedError()

    def all_pages(self):
        """Iterate over the titles of all pages in the wiki."""
        raise NotImplementedError()

    def changed_since(self, rev):
        """
        Return all pages that changed since specified repository revision.
        """
        raise NotImplementedError()

    def save_data(self, title, data, author=None, comment=None, parent_rev=None, ts=None, new=False):
        """Save a new revision of the page. If the data is None, deletes it."""
        _ = self._
        user = author or _('anon')
        text = comment or _('comment')

        ts = ts or datetime.datetime.utcnow()
        if data is None:
            if title not in self:
                raise error.ForbiddenErr()
            else:
                return self.delete_page(title, user, text, ts=ts)
        # else:
        #     if other is not None:
        #         try:
        #             data = self._merge(repo_file, parent, other, data)
        #         except ValueError:
        #             text = _(u'failed merge of edit conflict').encode('utf-8')
        return data, user, text, ts

    def save_text(self, title, text, author='', comment='', parent=None):
        """Save text as specified page, encoded to charset."""

        data = text.encode(self.charset)
        if self.unix_eol:
            data = data.replace(b'\r\n', b'\n')
        self.save_data(title, data, author, comment, parent)

    def page_text(self, title):
        """Read unicode text of a page."""
        data = self.page_data(title)
        text = str(data, self.charset, 'replace')
        return text

    def page_data(self, title):
        with self.open_page(title) as fp:
            data = fp.read()
            return data

    def page_meta(self, title):
        """Get page's revision, date, last editor and his edit comment."""
        return self.open_page(title, meta_only=True)

    def page_revision(self, title, rev):
        """Get binary content of the specified revision of the page."""
        try:
            with self.open_page(title, rev=rev) as fp:
                return fp.read()
        except FileNotFoundError:
            return b''

    def revision_text(self, title, rev):
        """Get unicode text of the specified revision of the page."""

        data = self.page_revision(title, rev)
        try:
            text = str(data, self.charset)
        except UnicodeDecodeError:
            text = self._('Unable to display')
        return text

    def __iter__(self):
        return self.all_pages()

    def _title_to_file(self, title):
        title = str(title).strip()
        filename = url_quote(title, safe='', unsafe='~')
        # Escape special windows filenames and dot files
        _windows_device_files = ('CON', 'AUX', 'COM1', 'COM2', 'COM3',
                                 'COM4', 'LPT1', 'LPT2', 'LPT3', 'PRN',
                                 'NUL')
        if (filename.split('.')[0].upper() in _windows_device_files or
            filename.startswith('_') or filename.startswith('.')):
            filename = '_' + filename
        if page.page_mime(title) == 'text/x-wiki' and self.extension:
            filename += self.extension
        return filename

    def _file_to_title(self, filepath):
        sep = os.path.sep
        name = filepath[len(self.repo_prefix):].strip(sep)
        # Un-escape special windows filenames and dot files
        if name.startswith('_') and len(name) > 1:
            name = name[1:]
        if self.extension and name.endswith(self.extension):
            name = name[:-len(self.extension)]
        return url_unquote(name)