import datetime
import os.path
import io
import re
import time
from hatta import error
from .base import BaseWikiStorage
from dulwich.objects import Blob, Tree, Commit
from dulwich.index import IndexEntry
from dulwich import porcelain


class WikiStorage(BaseWikiStorage):
    def __init__(self, repo_dir, **kwargs):
        super(WikiStorage, self).__init__(**kwargs)
        self.repo_path = repo_dir
        self.repo_prefix = self.repo_path[len(self.repo_path):].strip('/')
        self.reopen()

    def reopen(self):
        try:
            self.repo = porcelain.init(self.repo_path)
        except FileExistsError:
            self.repo = porcelain.open_repo(self.repo_path)
        self.object_store = self.repo.object_store
        self.control_dir = self.repo.controldir()
 
    def get_cache_path(self):
        return os.path.join(self.control_dir, 'cache')

    @property
    def index(self):
        return self.repo.open_index()

    def _path(self, title):
        path = os.path.abspath(os.path.join(self.repo.path, title))
        assert path.startswith(self.repo.path)
        return path.encode('utf8')

    def open_page(self, title, rev=None, meta_only=False):
        title = self._title_to_file(title).encode('utf8')
        try:
            entry = self.index[title]
        except KeyError:
            raise error.NotFoundErr()

        if not rev:
            rev = entry.sha
        else:
            rev = rev.encode('ascii')
        blob = self.object_store[rev]

        if not hasattr(blob, 'data'):
            for item in self.repo.get_walker(paths=[title], include=[rev]):
                blob_id = item.changes()[0].new.sha
                blob = self.object_store[blob_id]
                break
        return io.BytesIO(blob.data)

    def page_meta(self, title):
        title = self._title_to_file(title).encode('utf8')
        try:
            entry = self.index[title]
        except KeyError:
            raise error.NotFoundErr()
        rev = entry.sha
        if isinstance(entry.ctime, tuple):
            ctime = entry.ctime[0]
        else:
            ctime = entry.ctime
        ts = datetime.datetime.utcfromtimestamp(ctime)
        owner = comment = b''

        for item in self.repo.get_walker(paths=[title]):
            change = item.changes()[0]
            if change.new.sha == rev:
                owner = item.commit.author.decode('utf8')
                comment = item.commit.message.decode('utf8')
                break
        return rev.decode('ascii'), ts, owner, comment

    def _do_commit(self, index, author, message, ctime, parent_rev=None):
        index.write()
        committer = b'%s <>' % author.encode('utf8')
        commit = Commit()
        commit.tree = index.commit(self.object_store)
        commit.author = commit.committer = committer
        commit.commit_time = commit.author_time = ctime
        commit.encoding = b'UTF-8'
        commit.commit_timezone = commit.author_timezone = 0
        commit.message = message.encode('utf8')
        try:
            curr_head = self.repo.head()
            commit.parents = [curr_head]
            # if parent_rev and len(parent_rev) == 40:
            #     commit.parents.append(parent_rev.encode('ascii'))
        except KeyError:
            curr_head = None
        self.object_store.add_object(commit)
        self.repo.refs.set_if_equals(
                    b'HEAD', curr_head, commit.id, message=b"commit: " + commit.message,
                    committer=commit.committer, timestamp=ctime,
                    timezone=0)

    def save_data(self, title, data, author=None, comment=None, parent_rev=None, ts=None, new=False):
        data, user, text, created  = super(WikiStorage, self).save_data(
            title, data, author=author, comment=comment, parent_rev=parent_rev, ts=ts, new=new)
        ctime = mtime = int(created.timestamp())
        if data is not None:
            obj = Blob.from_string(data)
            self.object_store.add_object(obj)
            index = self.index
            index[self._title_to_file(title).encode('utf8')] = IndexEntry(
                ctime, mtime, 0,
                0, 0o100644, 1,
                1, len(data), obj.id, 0)
            self._do_commit(index, user, text, ctime, parent_rev=parent_rev)

    def delete_page(self, title, author, comment, ts=None):
        ts = ts or datetime.datetime.utcnow()
        index = self.index
        del index[self._title_to_file(title).encode('utf8')]
        self._do_commit(index, author, comment, int(ts.timestamp()))
        return None, author, comment, ts

    def all_pages(self):
        for path in self.index:
            yield self._file_to_title(path.decode('utf8'))

    def __contains__(self, title):
        if title:
            return self._title_to_file(title).encode('utf8') in self.index

    def repo_revision(self):
        try:
            return self.repo.head().decode('ascii')
        except KeyError:
            return None

    def _log_item(self, item):
        try:
            change = item.changes()[0]
        except IndexError:
            return {'title': '', 'rev': '', 'parent': '', 'date': None, 'author': None, 'comment': None}
        creation_date = datetime.datetime.utcfromtimestamp(item.commit.commit_time)
        owner = re.sub(' <.*>', '', item.commit.author.decode('utf8'))
        comment = item.commit.message.decode('utf8')
        if change.new.sha:
            rev = change.new.sha.decode('ascii')
            title = change.new.path.decode('utf8')
        else:
            rev = change.old.sha.decode('ascii')
            title = change.old.path.decode('utf8')

        if change.type != 'add':
            parent = change.old.sha.decode('ascii')
        else:
            parent = None
        return {
            'title': self._file_to_title(title),
            'rev': rev,
            'parent': parent,
            'date': creation_date,
            'author': owner,
            'comment': comment,
        }

    def page_history(self, title):
        last_item = None
        count = 0
        for item in self.repo.get_walker(paths=[self._title_to_file(title).encode('utf8')]):
            if last_item:
                last_item['parent'] = item.commit.id.decode('ascii')
                yield last_item
                count += 1
            last_item = self._log_item(item)
        if last_item:
            yield last_item

    def history(self):
        if self.repo_revision():
            for item in self.repo.get_walker():
                yield self._log_item(item)

    def changed_since(self, rev):
        if rev in (None, 'HEAD'):
            return self.all_pages()
        else:
            seen = set()
            for item in self.repo.get_walker(exclude=[rev.encode('utf8')]):
                item = self._log_item(item)
                if item['title'] not in seen:
                    yield item['title']
                    seen.add(item['title'])
