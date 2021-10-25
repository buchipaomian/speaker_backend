from configapp import app
from flask_restful import Api
import flask_restful as restful
from resource.login_management import Sign_up,Sign_in,Logout
from resource.audio_management import Audio_Link,Mixed_upload,Filter_generator,Text_result
from resource.embedder_management import Embedder_upload,Embedder_list,Embedder_Link

api = restful.Api(app)

api.add_resource(Sign_up,'/user/sign_up')
api.add_resource(Sign_in,'/user/sign_in')
api.add_resource(Logout,'/user/logout')

api.add_resource(Audio_Link,'/audio/<id>')
api.add_resource(Mixed_upload,'/upload/mixed')
api.add_resource(Filter_generator,'/filter')
api.add_resource(Text_result,'/to_text/<id>')
api.add_resource(Embedder_upload,'/upload/embedder')
api.add_resource(Embedder_list,'/embedder')
api.add_resource(Embedder_Link,'/embedder_audio/<id>')

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=4397)