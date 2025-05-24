import logging.config
import yaml
import os

def setup_logging(default_path='logging_config.yaml', default_level=logging.INFO):
    if os.path.exists(default_path):
        with open(default_path, 'r') as f:
            config = yaml.safe_load(f)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)


if __name__ == '__main__':  
    # Example usage
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("Logging is configured!")
    logger.debug("iterations")