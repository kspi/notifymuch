notifymuch
==========

This is a simple program that displays desktop notifications for unread
mail (or actually any search query) in the notmuch database. The notification
can optionally have a button to run a mail client.

When a message is shown in a notification, it is internally marked as 'recently
seen' and not shown again for two days (configurable).


Installation and usage
----------------------

The program requires Python 3, setuptools, pygobject and notmuch.
It can be installed together with its dependencies using::

    pip install .

To use, execute ``notifymuch`` after new mail is indexed (for example in a
*post-new* hook). The program forks and stays in the background while the
notification is active. If upon launch a notification is already active, it
is updated.


Configuration
-------------

Configuration is stored in ``~/.config/notifymuch/notifymuch.cfg``,
which is created on first run. Settings that can be set there:

query
  The notmuch search query for the messages. Default is
  ``is:unread and is:inbox``.
  
mail_client
  The command to launch the preferred mail client. If empty, the button
  isn't shown. Default is ``gnome-terminal -x mutt -y``.

recency_interval_hours
  Each message is notified about at most once in this time interval. Default is
  ``48``.

hidden_tags
  Tag names that are not shown in the notification. Default is
  ``inbox unread attachment replied sent encrypted signed``.
