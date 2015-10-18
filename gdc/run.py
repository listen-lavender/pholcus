#!/usr/bin/python
# coding=utf-8
from webcrawl.daemon import Daemon
from grab import task

path = os.path.abspath('.')

class PeriodMonitor(Daemon):

    def _run(self):
        task()

def main():
    moni = PeriodMonitor(os.path.join(path, 'log', 'moni.pid'), stdout=os.path.join(
        path, 'log', 'moni.out'), stderr=os.path.join(path, 'log', 'moni.err'))
    if os.path.exists(os.path.join(path, 'log', 'moni.pid')):
        print "PeriodMonitor stop successfully."
        moni.stop()
    else:
        print "PeriodMonitor start successfully."
        moni.start()

if __name__ == '__main__':
    main()
