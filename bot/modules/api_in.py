from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from bot.modules.manager import Manager_var, Task_M
# creating the flask app
APi = Flask(__name__)
# creating an API object
api = Api(APi)
  
# making a class for a particular resource
# the get, post methods correspond to get and post requests
# they are automatically mapped by flask_restful.
# other methods include put, delete, etc.
class Input(Resource):
  
    # corresponds to the GET request.
    # this function is called whenever there
    # is a GET request for this resource
    def get(self):
  
        return jsonify({'message': 'hello world'})
  
    # Corresponds to POST request
    def post(self):
        data:dict
        data = request.get_json()

        try:
            print('sendMessage :',data.get('sendMessage'))
        except:
            print('sendMessage Not Found')

        try:
            print('sendStatusMessage :',data.get('sendStatusMessage'))
        except:
            print('sendStatusMessage Not Found')

        try:
            print('Link :',data.get('Link'))
        except:
            print('Link Not Found')
        


        #SendMessage And Status
        if data.get('sendMessage',False) or data.get('sendStatusMessage',False) or data.get('Link',''):
            Hash = data.get('Hash')
            Task : Task_M
            Task = Manager_var.Get_Task_Class(Hash)
            if data.get('sendMessage',False) or data.get('Link',''):
                if data.get('Link'):
                    size = data.get('Size')
                    Link = data.get('Link')
                    text_msg = f'Your Link Generated At {Link}\n\nSize:{size}\n\nThanks'
                    Task.sendMessage_Task(text_msg)
                    del Manager_var.dict[Hash]
                else:
                    text_msg = data.get('text')
                    Task.sendMessage_Task(text_msg)
            elif data.get('sendStatusMessage',False):
                Task.sendStatusMessage_Task()
        
        return

api.add_resource(Input, '/')