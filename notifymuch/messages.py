from email.utils import parseaddr
import configparser
import os
import sys
import time
import xdg.BaseDirectory
import notmuch
from notifymuch.persistentdict import PersistentDict


__all__ = ["Messages"]


CACHE_DIR = xdg.BaseDirectory.save_cache_path('notifymuch')
CONFIG_DIR = xdg.BaseDirectory.save_config_path('notifymuch')

LAST_SEEN_FILE = os.path.join(CACHE_DIR, 'last_seen')
CONFIG_FILE = os.path.join(CONFIG_DIR, 'notifymuch' + '.cfg')

NONINTERESTING_TAGS = frozenset([
        'inbox', 'unread', 'attachment', 'replied', 'sent',
        'encrypted', 'signed'])


def exclude_recently_seen(messages):
    with PersistentDict(LAST_SEEN_FILE) as last_seen:
        now = time.time()
        for k in list(last_seen.keys()):
            if now - last_seen[k] > 60 * 60 * 24 * 2:  # Two days
                del last_seen[k]
        for message in messages:
            m_id = message.get_message_id()
            if m_id not in last_seen:
                last_seen[m_id] = now
                yield message


def filter_tags(ts):
    for t in ts:
        if t not in NONINTERESTING_TAGS:
            yield t


def ellipsize(text, length=80):
    if len(text) > length:
        return text[:length - 1] + '…'
    else:
        return text


def pretty_date(time=None):
    """
    Get a datetime object or a int() Epoch timestamp and return a
    pretty string like 'an hour ago', 'yesterday', '3 months ago',
    'just now', etc
    """
    from datetime import datetime
    now = datetime.now()
    if type(time) is int:
        diff = now - datetime.fromtimestamp(time)
    elif isinstance(time, datetime):
        diff = now - time
    elif not time:
        diff = now - now
    second_diff = diff.seconds
    day_diff = diff.days

    if day_diff < 0:
        return ''

    def ago(number, unit):
        if number == 1:
            return "a {unit} ago".format(unit=unit)
        else:
            return "{number} {unit}s ago".format(
                    number=round(number),
                    unit=unit)

    if day_diff == 0:
        if second_diff < 10:
            return "just now"
        if second_diff < 60:
            return ago(second_diff, "second")
        if second_diff < 120:
            return "a minute ago"
        if second_diff < 3600:
            return ago(second_diff / 60, "minute")
        if second_diff < 7200:
            return "an hour ago"
        if second_diff < 86400:
            return ago(second_diff / 60 / 60, "hour")
    if day_diff == 1:
        return "yesterday"
    if day_diff < 7:
        return ago(day_diff, "day")
    if day_diff < 31:
        return ago(day_diff / 7, "week")
    if day_diff < 365:
        return ago(day_diff / 30, "month")
    return ago(day_diff / 365, "year")


def pretty_sender(fromline):
    name, addr = parseaddr(fromline)
    return name or addr


def summary(messages):
    return '\n'.join('[{tags}] {subject} ({sender}, {date})'.format(
                subject=ellipsize(message.get_header('subject')),
                sender=pretty_sender(message.get_header('from')),
                date=pretty_date(message.get_date()),
                tags=' '.join(filter_tags(message.get_tags())))
            for message in messages)


class Messages:
    def __init__(self):
        config = configparser.ConfigParser()
        if not config.read(CONFIG_FILE):
            config['notifymuch'] = {'query': 'is:unread and is:inbox'}
            with open(CONFIG_FILE, "w") as f:
                config.write(f)

        db = notmuch.Database()
        self.query = notmuch.Query(db, config['notifymuch']['query'])
        self.query.set_sort(notmuch.Query.SORT.OLDEST_FIRST)

    def count(self):
        return self.query.count_messages()

    def messages(self):
        return self.query.search_messages()

    def summary(self):
        return summary(self.messages())

    def unseen_messages(self):
        return exclude_recently_seen(self.messages())

    def unseen_summary(self):
        return summary(self.unseen_messages())
