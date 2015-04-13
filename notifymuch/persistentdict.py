import pickle
import sys


class PersistentDict(dict):
    def __init__(self, filename):
        self.filename = filename

    def __enter__(self):
        try:
            with open(self.filename, 'rb') as f:
                self.update(pickle.load(f))
        except FileNotFoundError:
            pass
        except Exception as e:
            print("notifymuch: warning: {}".format(e), file=sys.stderr)
        return self

    def __exit__(self, type, value, traceback):
        with open(self.filename, 'wb') as f:
            pickle.dump(self, f)
