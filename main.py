import os
import logging
from bot import setup_and_run_bot
from keep_alive import keep_alive  # NEU
from typing import Union

def format_number(n: Union[float, int]) -> str:

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    token = os.environ.get("DISCORD_TOKEN")
    if not token:
        logger.error("DISCORD_TOKEN not found in environment variables.")
        exit(1)

    keep_alive()  # NEU: startet Webserver
    logger.info("Starting Discord bot...")
    setup_and_run_bot(token)
