import eel
import logging
import constants
import api.functions
from db.utils import setup as db_setup

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

def main():
    db_setup()

    eel.init(constants.FRONTEND_FOLDER)
    eel.start(constants.FRONTEND_INDEX_PAGE)

if __name__ == "__main__":
    main()