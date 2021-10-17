from sqliteModel import create_user, User,create_embedder_record
from flask_restful import abort, fields, reqparse, Resource
from itsdangerous.exc import BadSignature, SignatureExpired
from datetime import datetime
import json
from flask import send_from_directory
from resource.general import general_serializer, pwd_context, reset_password_link, activate_user_link
from werkzeug.datastructures import FileStorage
from process.tools import path_generater

profile_parser = reqparse.RequestParser()
profile_parser.add_argument(
    'token',
    dest='token',
    type=str,
    required=True,
    help='The token',
    location='headers',
)
profile_parser.add_argument('embedder',
                            dest='embedder',
                            type=FileStorage,
                            required=False,
                            help='The embedder',
                            location='files')
profile_parser.add_argument('name',
                            dest='name',
                            type=str,
                            required=False,
                            help='The name')


class Embedder_upload(Resource):
    #/upload/embedder
    def post(self):
        args = profile_parser.parse_args()
        token = args.token
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
        file = args.embedder
        name = args.name
        file_path = path_generater(name,"embedder")
        file.save(file_path)
        embedder_id = create_embedder_record(user,name,file_path)
        return {"status": True, "id":embedder_id, "name":name},200


class Embedder_list(Resource):
    #/embedder
    def get(self):
        args = profile_parser.parse_args()
        token = args.token
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
        embedder_list = []
        for k in user.embedder_records:
            embedder_list.append({'id': k.embedder_id, 'name': k.given_name})
        return embedder_list, 200

class Embedder_Link(Resource):
    #/embedder/<id>
    def get(self,id):
        args = profile_parser.parse_args()
        token = args.token
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
            if k.embedder_id == id:
                return send_from_directory("./",k.file_path, cache_timeout=0, as_attachment=True),200
        return {"error":"file not found, maybe it doesn't belong to you"},404

class Embedder_remove(Resource):
    #this may not required
    def post(self):
        pass