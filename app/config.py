import os


def map_level(level):
    """ Maps logging level strings to logging level codes

    Parameters:
        level (String): The level string to be mapped.

    Returns:
        Integer: Number that matches the logging level.
    """
    return {"critical": 50, "error": 40, "warning": 30, "info": 20, "debug": 10}.get(
        level, 10
    )


DATABASE_PATH = os.environ.get("DATABASE_PATH", "app.db")
LOGGING_LEVEL = map_level(os.environ.get("LOGGING_LEVEL", "debug"))
MAX_TERMS = int(os.environ.get("MAX_TERMS", "1"))
PROJECT_DIR = os.path.abspath(os.curdir)
PROCESSED_BUCKET_NAME = os.environ.get("BUCKET_NAME", "pdx-schedule-processed-data")
