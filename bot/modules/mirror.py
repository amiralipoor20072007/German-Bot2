from telegram.ext import CommandHandler , extbot
from time import sleep
from base64 import b64encode
from threading import Thread
from re import match as re_match, split as re_split
from os import path as ospath
from time import sleep, time
from threading import Thread
from telegram.ext import CommandHandler
from requests import get as rget

from bot import dispatcher, LOGGER
from bot.helper.bot_commands import BotCommands
from bot.helper.bot_utils import is_url, is_magnet, is_mega_link, is_gdrive_link, get_content_type
from bot.helper.direct_link_generator import direct_link_generator
from bot.helper.exceptions import DirectDownloadLinkException
from bot.helper.message_utils import sendMessage
from bot.modules.manager import Manager_var

def _mirror_leech(bot, message,isQbit=False):
    mesg = message.text.split('\n')
    message_args = mesg[0].split(maxsplit=1)
    index = 1
    multi = 0
    link = ''
    folder_name = ''

    if len(message_args) > 1:
        args = mesg[0].split(maxsplit=4)
        for x in args:
            x = x.strip()
            if x in ['|', 'pswd:']:
                break
            elif x == 's':
               select = True
               index += 1
            elif x == 'd':
                seed = True
                index += 1
            elif x.startswith('d:'):
                seed = True
                index += 1
                dargs = x.split(':')
                ratio = dargs[1] if dargs[1] else None
                if len(dargs) == 3:
                    seed_time = dargs[2] if dargs[2] else None
            elif x.isdigit():
                multi = int(x)
                mi = index
            elif x.startswith('m:'):
                marg = x.split('m:', 1)
                if len(marg) > 1:
                    folder_name = f"/{marg[-1]}"
                    if not sameDir:
                        sameDir = set()
                    sameDir.add(message.message_id)
        if multi == 0:
            message_args = mesg[0].split(maxsplit=index)
            if len(message_args) > index:
                link = message_args[index].strip()
                if link.startswith(("|", "pswd:")):
                    link = ''
        if len(folder_name) > 0:
            seed = False
            ratio = None
            seed_time = None

    def __run_multi():
        if multi > 1:
            sleep(4)
            nextmsg = type('nextmsg', (object, ), {'chat_id': message.chat_id,
                                                   'message_id': message.reply_to_message.message_id + 1})
            msg = message.text.split(maxsplit=mi+1)
            msg[mi] = f"{multi - 1}"
            nextmsg = sendMessage(" ".join(msg), bot, nextmsg)
            if len(folder_name) > 0:
                sameDir.add(nextmsg.message_id)
            nextmsg.from_user.id = message.from_user.id
            sleep(4)
            Thread(target=_mirror_leech, args=(bot, nextmsg)).start()

    name = mesg[0].split('|', maxsplit=1)
    if len(name) > 1:
        if 'pswd:' in name[0]:
            name = ''
        else:
            name = name[1].split('pswd:')[0].strip()
    else:
        name = ''

    pswd = mesg[0].split(' pswd: ')
    pswd = pswd[1] if len(pswd) > 1 else None

    if message.from_user.username:
        tag = f"@{message.from_user.username}"
    else:
        tag = message.from_user.mention_html(message.from_user.first_name)

    if link != '':
        link = re_split(r"pswd:|\|", link)[0]
        link = link.strip()

    reply_to = message.reply_to_message
    if reply_to is not None:
        file_ = reply_to.document or reply_to.video or reply_to.audio or reply_to.photo or None
        if not reply_to.from_user.is_bot:
            if reply_to.from_user.username:
                tag = f"@{reply_to.from_user.username}"
            else:
                tag = reply_to.from_user.mention_html(reply_to.from_user.first_name)
        if len(link) == 0 or not is_url(link) and not is_magnet(link):
            if file_ is None:
                reply_text = reply_to.text.split(maxsplit=1)[0].strip()
                if is_url(reply_text) or is_magnet(reply_text):
                    link = reply_to.text.strip()
            elif isinstance(file_, list):
                link = file_[-1].get_file().file_path
            elif not isQbit and file_.mime_type != "application/x-bittorrent":
                return
            else:
                link = file_.get_file().file_path

    if not is_url(link) and not is_magnet(link):
        help_msg = '''
<code>/cmd</code> link |newname pswd: xx(zip/unzip)

<b>By replying to link/file:</b>
<code>/cmd</code> |newname pswd: xx(zip/unzip)

<b>Direct link authorization:</b>
<code>/cmd</code> link |newname pswd: xx(zip/unzip)
<b>username</b>
<b>password</b>

<b>Bittorrent selection:</b>
<code>/cmd</code> <b>s</b> link or by replying to file/link
This option should be always before |newname or pswd:

<b>Bittorrent seed</b>:
<code>/cmd</code> <b>d</b> link or by replying to file/link
To specify ratio and seed time add d:ratio:time. Ex: d:0.7:10 (ratio and time) or d:0.7 (only ratio) or d::10 (only time) where time in minutes.
Those options should be always before |newname or pswd:

<b>Multi links only by replying to first link/file:</b>
<code>/cmd</code> 10(number of links/files)
Number should be always before |newname or pswd:

<b>Multi links within same upload directory only by replying to first link/file:</b>
<code>/cmd</code> 10(number of links/files) m:folder_name
Number and m:folder_name should be always before |newname or pswd:

<b>NOTES:</b>
1. When use cmd by reply don't add any option in link msg! always add them after cmd msg!
2. You can't add those options <b>|newname, pswd:</b> randomly. They should be arranged like exmaple above, rename then pswd. Those options should be after the link if link along with the cmd and after any other option
3. You can add those options <b>d, s and multi</b> randomly. Ex: <code>/cmd</code> d:1:20 s 10 <b>or</b> <code>/cmd</code> s 10 d:0.5:100
4. Commands that start with <b>qb</b> are ONLY for torrents.
'''

        sendMessage(help_msg, bot, message)
        return

    LOGGER.info(link)

    if not is_mega_link(link) and not isQbit and not is_magnet(link) \
        and not is_gdrive_link(link) and not link.endswith('.torrent'):
        content_type = get_content_type(link)
        if content_type is None or re_match(r'text/html|text/plain', content_type):
            try:
                link = direct_link_generator(link)
                LOGGER.info(f"Generated link: {link}")
            except DirectDownloadLinkException as e:
                LOGGER.info(str(e))
                if str(e).startswith('ERROR:'):
                    sendMessage(str(e), bot, message)
                    __run_multi()
                    return
    elif isQbit and not is_magnet(link):
        return

    if is_gdrive_link(link):
        return
    elif is_mega_link(link):
        return
    elif isQbit and (is_magnet(link) or ospath.exists(link)):
        return
    else:
        if len(mesg) > 1:
            ussr = mesg[1]
            if len(mesg) > 2:
                pssw = mesg[2]
            else:
                pssw = ''
            auth = f"{ussr}:{pssw}"
            auth = "Basic " + b64encode(auth.encode()).decode('ascii')
        else:
            auth = ''
        Managser = Manager_var.Add_Task(message,bot,link,name,auth)
        Thread(target=Managser.Send_Command).start()
    __run_multi()

def mirror(update, context):
    _mirror_leech(context.bot, update.message)

mirror_handler = CommandHandler(BotCommands.MirrorCommand, mirror)

dispatcher.add_handler(mirror_handler)