import eel
import logging
import constants
import api.functions # import all eel functions to main applicaiton
from db.utils import setup as db_setup
import ollama

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    logger.info("Setting up the database")
    db_setup()
    logger.info("Pulling the LLM model")
    ollama.pull(constants.LLM_MODEL)

    logger.info("Starting the EEL application")
    eel.init(constants.FRONTEND_FOLDER)
    eel.start(constants.FRONTEND_INDEX_PAGE)

if __name__ == "__main__":
    main()