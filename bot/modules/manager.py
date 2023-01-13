from requests import post as rpost
from random import choices
import string

from bot import LOGGER
from bot.helper.message_utils import sendMessage , sendStatusMessage


class Manager():
    def __init__(self) -> None:
        self.dict = {}

    def Add_Task(self,msg=None,bot='',link='',filename='',auth=''):
        Hash = ''.join(choices(string.ascii_lowercase,k=12))
        Task = Task_M(msg,bot,link,Hash,filename,auth)
        self.dict[Hash] = Task
        return Task

    def Get_Task_Class(self,Hash):
        if Hash in self.dict:
            return self.dict.get(Hash)

class Task_M():
    def __init__(self,msg,bot,link,Hash,filename,auth) -> None:
        self.chat_id = msg.chat.id
        self.Hash = Hash
        self.message_id = msg.message_id
        self.message = msg
        self.filename = filename
        self.auth = auth
        self.bot = bot
        self.link = link
    
    def Send_Command(self):
        rpost('http://45.159.149.18:5000',json={'link': self.link,'chat_id':self.chat_id,
         'ServerHash':self.Hash, 'filename':self.filename, 'auth':self.auth})

    def sendMessage_Task(self,text):
        sendMessage(text,self.bot,self.message)

    def sendStatusMessage_Task(self):
        sendStatusMessage(self.message,self.bot)

Manager_var = Manager()

    


        