import sys
import signal
import logging
import pymongo
import datetime

logging.basicConfig(level=logging.DEBUG)

def signal_handler(signal, frame):
    """
    I'm unsure how/if this will work in Windows...
    """
    print "\nCtrl+C -- Quitting current weather tail"
    sys.exit(0)


class MongoTail(object):

    def __init__(self, loc='London'):
        c = pymongo.MongoClient()
        self.db = c.openweathermap
        self.collection = self.db.current[loc]

    def tail(self):

        cursor = self.collection.find(tailable=True,
                                      await_data=True,
                                      timeout=False)

        while cursor.alive:
            try:
                record = cursor.next()
                print "\n", datetime.datetime.now(), "- latest record"
                print record
            except StopIteration:
                #print "stopping"
                pass


def main():
    m = MongoTail()
    m.tail()


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    main()
