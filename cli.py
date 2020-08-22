import os
import logging

from gui.main import (
    run,
)

if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s %(message)s',
        handlers=[
            logging.FileHandler(os.path.join(os.path.expanduser(os.path.join("~", "Documents", "WAM")), "session.log")),
            logging.StreamHandler()
            ]
        )
    logging.debug('This message should go to the log file and to the console')
    logging.info('So should this')
    logging.warning('And this, too')

    try:
        run() # app()
    except:
        logging.exception('Exception caught')
        raise
