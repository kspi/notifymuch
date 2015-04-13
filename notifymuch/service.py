import os
from gi.repository import Notify, GLib
import dbus
import dbus.bus
import dbus.service
import dbus.mainloop.glib
from notifymuch.messages import Messages


__all__ = ["show_notification"]


DBUS_NAME = 'net.wemakethings.NotifymuchService'


class NotifymuchService(dbus.service.Object):
    ICON = '/usr/share/icons/gnome/scalable/status/mail-unread-symbolic.svg'

    def __init__(self, bus, path, name):
        dbus.service.Object.__init__(self, bus, path, name)
        Notify.init('notifymuch')
        self.main_loop = GLib.MainLoop()
        self.notification = Notify.Notification.new('', '', self.ICON)
        self.notification.set_timeout(Notify.EXPIRES_NEVER)
        self.notification.add_action('mutt', 'Run Mutt', self.action_mutt)
        self.notification.connect('closed', lambda e: self.exit())

    def exit(self):
        self.main_loop.quit()

    def action_mutt(self, action, user_data):
        os.execvp("gnome-terminal", ["gnome-terminal", "-x", "mutt", "-y"])

    @dbus.service.method(DBUS_NAME, in_signature='', out_signature='')
    def update(self):
        try:
            messages = Messages()
            summary = messages.unseen_summary()
            if summary == "":
                self.exit()
            else:
                self.notification.update(
                        summary="{count} unread messages".format(
                            count=messages.count()),
                        body=messages.summary(),
                        icon=self.ICON)
                self.notification.show()
        except:
            self.exit()
            raise

    @dbus.service.method(DBUS_NAME, in_signature='', out_signature='')
    def run(self):
        GLib.idle_add(self.update)
        self.main_loop.run()


def show_notification():
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    bus = dbus.SessionBus()
    request = bus.request_name(DBUS_NAME, dbus.bus.NAME_FLAG_DO_NOT_QUEUE)
    if request == dbus.bus.REQUEST_NAME_REPLY_EXISTS:
        obj = bus.get_object(DBUS_NAME, "/")
        app = dbus.Interface(obj, DBUS_NAME)
        app.update()
    elif os.fork() == 0:
        app = NotifymuchService(bus, '/', DBUS_NAME)
        app.run()
