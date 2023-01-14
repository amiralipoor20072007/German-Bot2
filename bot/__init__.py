from asyncio import get_event_loop
from time import time
from threading import Lock
from telegram.ext import Updater as tgUpdater, Defaults
from logging import getLogger, FileHandler, StreamHandler, INFO, basicConfig, error as log_error, info as log_info, warning as log_warning
basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[FileHandler('log.txt'), StreamHandler()],
                    level=INFO)
main_loop = get_event_loop()
LOGGER = getLogger(__name__)
Interval = []
download_dict_lock = Lock()
status_reply_dict_lock = Lock()
queue_dict_lock = Lock()
# Key: update.effective_chat.id
# Value: telegram.Message
status_reply_dict = {}
# Key: update.message.message_id
# Value: An object of Status
download_dict = {}
botStartTime = time()
user_data = {}
BASE_URL = ''
WEB_PINCODE = False
STATUS_LIMIT = 5
DOWNLOAD_DIR = '/usr/src/app/downloads/'

config_dict = {'BASE_URL': BASE_URL,
               'DOWNLOAD_DIR': DOWNLOAD_DIR,
               'STATUS_LIMIT': STATUS_LIMIT,
               'WEB_PINCODE': WEB_PINCODE,
               'STATUS_UPDATE_INTERVAL' : 5}

BOT_TOKEN = '5556552657:AAFll3gaZEAlYdDYtPOMcIaOj906rnPo8EU'
if len(BOT_TOKEN) == 0:
    log_error("BOT_TOKEN variable is missing! Exiting now")
    exit(1)
DATABASE_URL = ''
# if len(DATABASE_URL) == 0:
#     log_error("DATABASE_URL variable is missing! Exiting now")
    # exit(1)

bot_id = int(BOT_TOKEN.split(':', 1)[0])

tgDefaults = Defaults(parse_mode='HTML', disable_web_page_preview=True, allow_sending_without_reply=True, run_async=True)
updater = tgUpdater(token=BOT_TOKEN, defaults=tgDefaults, request_kwargs={'read_timeout': 20, 'connect_timeout': 15})
bot = updater.bot
dispatcher = updater.dispatcher
job_queue = updater.job_queue