class OSS:
    """An OS mimicker."""

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def __init__(self, ram_max, disks_max):
        self._num_of_ram = ram_max
        self._num_of_disks = disks_max

    def process(self, command, size):
        print('process', command, size)

    def hard_disk(self, command, number):
                print('hard disk', command, number)

    def show(self, show_type):
        if(show_type == 'r'):
            pass
        elif(show_type == 'i'):
            pass
        elif(show_type == 'm'):
            pass
        print('show', show_type)

    def time(self, command):
        print('time', command)
