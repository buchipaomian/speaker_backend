from sqliteModel import create_audio_record, create_user,Audio_Record,User
from flask_restful import abort, fields, reqparse, Resource
from itsdangerous.exc import BadSignature, SignatureExpired
from datetime import datetime
import json
from flask import send_from_directory
from resource.general import general_serializer,pwd_context,reset_password_link,activate_user_link
from werkzeug.datastructures import FileStorage
from process.tools import path_generater,generate_random_file_path
from process.speech2text import model,speech_to_text
from process.voicefilter import voice_model,voice_embedder,voice_filter
import os
import librosa
import soundfile as sf

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
        First_Path,Second_Name=os.path.split(file_path)
        return send_from_directory(First_Path,Second_Name, cache_timeout=0, as_attachment=True)
        

class Mixed_upload(Resource):
    #/upload/mixed
    def post(self):
        #here we pretend we do not need login,
        #but in fact we need, I just won't check it for now
        args = audio_parser.parse_args()
        file = args.audio
        file_type = file.filename.split('.')[-1]
        file_path = generate_random_file_path("mixed",file_type)
        file.save(file_path)
        audio_id = create_audio_record(file_path)
        return {"id":audio_id},200


filter_parser = reqparse.RequestParser()
filter_parser.add_argument(
    'token',
    dest='token',
    type=str,
    required=True,
    help='The token',
    location='headers',
)
filter_parser.add_argument('audio_id',
                            dest='audio_id',
                            type=str,
                            required=True,
                            help='The audio id')
filter_parser.add_argument('embedder_id',
                            dest='embedder_id',
                            type=str,
                            required=True,
                            help='The embedder id')

class Filter_generator(Resource):
    #/filter
    def post(self):
        args = filter_parser.parse_args()
        #here we suppose to check the token, but maybe later
        token = args.token
        audio_id = args.audio_id
        embedder_id = args.embedder_id
        try:
            data = general_serializer.loads(token)
        except SignatureExpired:
            return {"error": "login failed"}, 401  # valid token, but expired
        except BadSignature:
            return {"error": "login failed"}, 401
        user_email = data["useremail"]
        user = User.query.filter_by(user_email=user_email).first()
        if not user:
            return {"error": "login failed"}, 401
        if not user.user_activate:
            return {"error": "login failed"}, 400
        if user.user_last_token != token:
            return {"error": "login failed"}, 401
        for k in user.embedder_records:
            if k.embedder_id == int(embedder_id):
                #todo: maybe need to check if the id is int
                embedder_file_path = k.file_path
        audio_record = Audio_Record.query.filter_by(audio_id=audio_id).first()
        if not audio_record:
            return {"error":"file not found"},404
        audio_file_path = audio_record.file_path
        reference_wav,_ = librosa.load(embedder_file_path, sr=16000)
        mixed_wav,_ = librosa.load(audio_file_path, sr=16000)
        result_wav = voice_filter(reference_wav,mixed_wav,voice_model,voice_embedder)
        file_type = 'wav'
        result_file_path = generate_random_file_path("result",file_type)
        audio_id = create_audio_record(result_file_path)
        sf.write(result_file_path, result_wav, 16000)
        return {'id':audio_id}

class Text_result(Resource):
    #/to_text/<id>
    def get(self,id):
        audio_record = Audio_Record.query.filter_by(audio_id=id).first()
        if not audio_record:
            return {"error":"file not found"},404
        file_path = audio_record.file_path
        text = speech_to_text(file_path,model)
        return {"status":"done",'text':text},200