import sys
import os
from gi.repository import Notify, Gio
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
        Notify.init('notifymuch')
        self.notification = Notify.Notification.new('', '', self.ICON)
        self.notification.set_timeout(Notify.EXPIRES_NEVER)
        self.notification.add_action('mutt', 'Run Mutt', self.action_mutt)
        self.notification.connect('closed', lambda e: self.release())

    def on_activate(self, data):
        messages = Messages()
        summary = messages.unseen_summary()
        if summary != "":
            self.hold()
            self.notification.update(
                    summary="{count} unread messages".format(
                        count=messages.count()),
                    body=summary,
                    icon=self.ICON)
            self.notification.show()

    def action_mutt(self, action, data):
        self.notification.close()
        self.quit()
        if os.fork() == 0:
            os.execvp("gnome-terminal", ["gnome-terminal", "-x", "mutt", "-y"])


def show_notification():
    # Gio.Application.run blocks in case this is the primary instance, and
    # returns immediately otherwise. We fork here so that it never blocks.
    if os.fork() == 0:
        sys.exit(NotifymuchNotification().run())
