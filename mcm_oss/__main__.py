import cli


def main():
    '''
    Execute some helpful information about program and then start interactive
    cli.
    '''
    print('''
Welcome to mcm-oss: A simple and basic operating system simulation.

Some commands implemented:
  A  size    creates a new common process
  AR size    the same as 'A #size' but the new process is an RT-process
  Q          ends the time slice for the currently running process
  t          terminates the currently running process
  d  number  process that currently uses the CPU requests the hard disk #number
  D  number  hard disk #number finishes the work for one process
  S  r       shows state of the process queue
  S  i       shows state of the disks
  S  m       shows state of the memory

The way this cli utility handles signals:
    KeyboardInterrupt - Ctrl+c - exits current command
    EOFError          - Ctrl+d - exits program
    ''')
    cli.interactive()


if __name__ == '__main__':
    main()
