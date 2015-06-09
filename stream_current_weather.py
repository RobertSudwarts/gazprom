"""
This module streams data from the HTTP request to a mongodb
From the command line, you could inspect as follows:
   > show dbs;
   > use openweathermap;
   > show collections;
   > db.current.London.find()

As records are being simply dumped in, the *last* record inserted is trivial
(and optimal) to find using a sort on the automatically generated `_id`
(as the timestamp is effectively recorded in the indexed ObjectID)

   > db.current.London.find().sort({$natural : -1}).limit(1);

From python (and even better!) we can query the tail:
see tail_current_weather.py
"""
import sys
import signal
import time
import utils
import logging
import pymongo

import openweathermap_requests as ow

logging.basicConfig(level=logging.DEBUG)

WAIT = 2 * 60
SIZE = 50000

def signal_handler(signal, frame):
    """
    I'm unsure how/if this will work in Windows...
    """
    print "\nCtrl+C -- Quitting current weather stream"
    sys.exit(0)


class MongoStream(object):

    def __init__(self, loc='London'):
        c = pymongo.MongoClient()
        self.db = c.openweathermap

        if 'current.%s' % loc not in self.db.collection_names():
            logging.info("creating collection")
            self.create_collection(loc)
            self.collection = self.db.current[loc]
        else:
            logging.info("collection exists!")
            self.collection = self.db.current[loc]
            logging.debug("collection is capped: %s", self.is_capped)

    @property
    def is_capped(self):
        opts = self.collection.options()
        if 'capped' in opts and opts['capped']:
            return True
        else:
            return False

    def create_collection(self, loc):
        logging.info("creating capped collection")
        self.db.create_collection(
            'current.%s' % loc,
            capped=True,
            size=SIZE
            )

    def stream(self):
        last_ts = None
        while True:
            data = ow.current_weather_req()
            this_ts = utils.ts(data['dt'])
            logging.debug("%s --> %s", last_ts, this_ts)
            if last_ts != this_ts:
                logging.info("adding record to database")
                self.collection.insert(data)
            else:
                logging.debug("no change")

            last_ts = this_ts
            time.sleep(WAIT)


def main():
    """
    notice that we're making use of pymongo's access to a sub-collection
    using dot *AND* dict notation -- `current` here could be substituted with
    'forecast' and the location (eg London) would be a parameter passed into
    `main()`

    This could be accomplished just as easily by indexing the location and
    querying accordingly however a sub-collection makes for a cleaner structure
    """
    m = MongoStream()
    m.stream()


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    main()
