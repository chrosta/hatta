This is a fork of [Hatta Wiki](http://hatta-wiki.org), with these changes:
* supports python 3 only and Mercurial version 5.4+,
* supports using git repositories,
* uses whoosh for the search index.

To install:
`pip install git+https://github.com/davestgermain/hatta.git`
.

To run against a git repo instead of mercurial:
`python -m hatta -d /some/repo -v git`
.

My appearance hacks for Hatta:
* name of the document in URL is formated always with a first capital letter,
* path in URL is formated to lower case,
* buttons and links (to brackets) redesign,
* titles redesign.
