from sqliteModel import create_user
from flask_restful import abort, fields, reqparse, Resource
from itsdangerous.exc import BadSignature, SignatureExpired
from datetime import datetime
import json
from resource.general import general_serializer,pwd_context,reset_password_link,activate_user_link

user_parser = reqparse.RequestParser()
user_parser.add_argument(
    'user_email',
    dest='user_email',
    type=str,
    required=True,
    help='The user email',
)
user_parser.add_argument(
    'user_password',
    dest='user_password',
    type=str,
    required=True,
    help='The user password, should be coded',
)


class Sign_up(Resource):
    def post(self):
        args = user_parser.parse_args()
        user_infor = {}
        user_infor["email"] = args.user_email
        user_password = args.user_password
        user_infor["password"] = pwd_context.hash(user_password)
        result = create_user(user_infor)
        if result:
            """
            target_email = args.user_email
            #here will add email auth function
            data = {
                "useremail": target_email,
            }
            token = general_serializer.dumps(data).decode('ascii')
            # we can send the token
            # msg = "Dear Mr/Ms/Mrs, \n this link is to activate your account, do not share the link with anyone else.\n link: "+activate_user_link+token
            # result = send_alert(msg,target_email)
            if result:
                return {"infor":"an activate email have send to your address"},200
            else:
                print("error happend")
                return {"infor":"an email have send to your address"},200
            """
            return {"infor":"register finished"},200
        else:
            return {"error": "user already exist"}, 400


class Sign_in(Resource):
    def verify_password(self, plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    def post(self):
        args = user_parser.parse_args()
        user_email = args.user_email
        user_password = args.user_password
        user = User.query.filter_by(user_email=user_email).first()
        if not user:
            return {"error": "login failed"}, 400
        if not user.user_activate:
            return {"error": "login failed"}, 400
        if not self.verify_password(user_password, user.user_password):
            return {"error": "login failed"}, 400
        data = {
            "useremail": user.user_email,
        }
        token = general_serializer.dumps(data).decode('ascii')
        user.user_last_token = token
        user.user_last_activate_time = datetime.now()
        Update_database()
        expiry_timestamp = int(datetime.now().timestamp() + 3600)
        return {
            "token": token,
            "useremail": str(user.user_email),
            "access_token": token,
            "expiry_timestamp": expiry_timestamp
        }


token_parser = reqparse.RequestParser()
token_parser.add_argument(
    'token',
    dest='token',
    type=str,
    required=True,
    help='The token',
    location='headers',
)
token_parser.add_argument(
    'sp_secrect',
    dest='sp_secrect',
    type=str,
    required=False,
    help='The sp_secrect',
)


class Logout(Resource):
    def post(self):
        args = token_parser.parse_args()
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
        user.user_last_token = None
        Update_database()
        return {"infor": "logout finished"}, 200
