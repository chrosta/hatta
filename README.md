This is a fork of [Hatta Wiki](http://hatta-wiki.org), with these changes:
* supports python 3 only and Mercurial version 5.4+,
* supports using git repositories,
* uses whoosh for the search index.

To install:
`pip install git+https://github.com/davestgermain/hatta.git`,
respectively `pip install git+https://github.com/chrosta/hatta.git`.

To run against a git repo instead of mercurial:
`python -m hatta -d /some/repo -v git`.

Alternative amateur deploy (something like):
`mkdir $HOME/Hatta; cd $HOME/Hatta/`, 
`mkdir -p ./repos/default`, 
`git clone https://github.com/chrosta/hatta`, 
`cd /usr/local/lib/python3.10/site-packages/`, 
`sudo ln -s $HOME/Hatta/hatta/hatta hatta`, 
`python -m hatta -d $HOME/Hatta/repos/default -v git`.

Use root/sudo privileges (if it's necessary).
Try running it, install necessary Python libraries (and happy hacking).

My appearance hacks for Hatta:
* first word of document name in URL is formatted always to lower letters,
* path in URL is formated to lower case,
* buttons and links (to brackets) redesign,
* titles redesign, CSS and JS hacks.
