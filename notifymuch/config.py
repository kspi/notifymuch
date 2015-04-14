import os
import configparser
import xdg.BaseDirectory


__all__ = ['load', 'get']


CONFIG_DIR = xdg.BaseDirectory.save_config_path('notifymuch')
CONFIG_FILE = os.path.join(CONFIG_DIR, 'notifymuch' + '.cfg')

DEFAULT_CONFIG = {
    'query': 'is:unread and is:inbox',
    'mail_client': 'gnome-terminal -x mutt -y',
}

CONFIG = configparser.ConfigParser()


def load():
    global CONFIG
    CONFIG['notifymuch'] = DEFAULT_CONFIG
    if not CONFIG.read(CONFIG_FILE):
        with open(CONFIG_FILE, "w") as f:
            CONFIG.write(f)


def get(option):
    return CONFIG['notifymuch'][option]
