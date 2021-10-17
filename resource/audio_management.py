from sqliteModel import create_user,Audio_Record
from flask_restful import abort, fields, reqparse, Resource
from itsdangerous.exc import BadSignature, SignatureExpired
from datetime import datetime
import json
from flask import send_from_directory
from resource.general import general_serializer,pwd_context,reset_password_link,activate_user_link
from werkzeug.datastructures import FileStorage
from process.tools import path_generater

audio_parser = reqparse.RequestParser()
audio_parser.add_argument(
    'token',
    dest='token',
    type=str,
    required=False,
    help='The token',
    location='headers',
)
audio_parser.add_argument('audio',
                            dest='audio',
                            type=FileStorage,
                            required=False,
                            help='The mixed audio',
                            location='files')
audio_parser.add_argument('name',
                            dest='name',
                            type=str,
                            required=False,
                            help='The name')

class Audio_Link(Resource):
    #/audio/<id>
    def get(self,id):
        audio_record = Audio_Record.query.filter_by(audio_id=id).first()
        if not audio_record:
            return {"error":"file not found"},404
        file_path = audio_record.file_path
        return send_from_directory("./",file_path, cache_timeout=0, as_attachment=True),200
        

class Mixed_upload(Resource):
    #/upload/mixed
    def post(self):
        #here we pretend we do not need login,
        #but in fact we need, I just won't check it for now
        pass

class Filter_generator(Resource):
    #/filter
    def post(self):
        pass

class Text_result(Resource):
    #/to_text
    def get(self):
        pass