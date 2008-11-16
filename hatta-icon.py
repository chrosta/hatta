#!/usr/bin/python
# -*- coding: utf-8 -*-

import hatta
import werkzeug
import gtk
import webbrowser
import os

class StatusIcon(object):
    def __init__(self, config):
        host = config.interface or 'localhost'
        port = int(config.port)
        self.url = 'http://%s:%d/' % (host, port)
        loader = gtk.gdk.PixbufLoader()
        loader.write(config.icon)
        loader.close()
        self.icon = gtk.StatusIcon()
        self.icon.set_from_pixbuf(loader.get_pixbuf())
        self.icon.set_tooltip('Hatta Wiki')
        self.icon.connect_object('activate', self.on_activate, None)
        self.icon.connect_object('popup-menu', self.on_popup, None)

    def on_activate(self, status_icon, data=None):
        webbrowser.open('http://localhost:8080')

    def on_popup(self, status_icon, button, activate_time):
        menu = gtk.Menu()
        browser = gtk.ImageMenuItem(gtk.STOCK_OPEN)
        browser.connect('activate', self.on_activate, False)
        quit = gtk.ImageMenuItem(gtk.STOCK_CLOSE)
        quit.connect('activate', self.quit_on_activate, False)
        menu.append(browser)
        menu.append(quit)
        menu.show()
        browser.show()
        quit.show()
        menu.popup(None, None, None, button, activate_time)

    def quit_on_activate(self, item, data=None):
        gtk.main_quit()

if __name__ == "__main__":
    config = hatta.WikiConfig(
        # Here you can modify the configuration: uncomment and change the ones
        # you need. Note that it's better use environment variables or command
        # line switches.

        # interface=''
        # port=8080
        # pages_path = 'docs'
        # cache_path = 'cache'
        # front_page = 'Home'
        # site_name = 'Hatta Wiki'
        # page_charset = 'UTF-8'
    )
    config._parse_args()
    application = hatta.Wiki(config).application
    pid = os.fork()
    try:
        if not pid:
            werkzeug.run_simple(config.interface, int(config.port), application,
                                use_reloader=True)
        elif os.environ.get("WERKZEUG_RUN_MAIN") == 'true':
            status_icon = StatusIcon(config)
            gtk.main()
            os.kill(pid, 2)
            os.waitpid(pid, 0)
    except KeyboardInterrupt:
        pass