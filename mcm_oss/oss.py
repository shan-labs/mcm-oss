class OSS:
    """An OS mimicker."""

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def __init__(self, ram_max, disks_max):
        self._ram = [None] * ram_max
        self._disks = [None] * disks_max

    def show(self, show_type):
        print(self._ram, self._disks, show_type)
