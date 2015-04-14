import sys
import os
import shlex
from gi.repository import Notify, Gio
from notifymuch import config
from notifymuch.messages import Messages


__all__ = ["show_notification"]


class NotifymuchNotification(Gio.Application):
    ICON = '/usr/share/icons/gnome/scalable/status/mail-unread-symbolic.svg'

    def __init__(self):
        Gio.Application.__init__(
                self,
                application_id="net.wemakethings.Notifymuch",
                flags=Gio.ApplicationFlags.FLAGS_NONE)
        self.connect('startup', self.on_startup)
        self.connect('activate', self.on_activate)

    def on_startup(self, data):
        config.load()
        Notify.init('notifymuch')
        self.notification = Notify.Notification.new('', '', self.ICON)
        self.notification.set_timeout(Notify.EXPIRES_NEVER)
        if config.get("mail_client"):
            self.notification.add_action('mail-client', 'Run mail client', self.action_mail_client)
        self.notification.connect('closed', lambda e: self.release())
        self.hold()

    def on_activate(self, data):
        config.load()
        messages = Messages()
        summary = messages.unseen_summary()
        if summary != "":
            self.notification.update(
                    summary="{count} unread messages".format(
                        count=messages.count()),
                    body=summary,
                    icon=self.ICON)
            self.notification.show()

    def action_mail_client(self, action, data):
        self.notification.close()
        tokens = shlex.split(config.get("mail_client"))
        if os.fork() == 0:
            os.execvp(tokens[0], tokens)


def show_notification():
    # Gio.Application.run blocks in case this is the primary instance, and
    # returns immediately otherwise. We fork here so that it never blocks.
    if os.fork() == 0:
        sys.exit(NotifymuchNotification().run())
