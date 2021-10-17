from configapp import db
import logging_loader
from datetime import datetime

logger = logging_loader.Logger(name="mysql_logger",logname='log/mysql.log').logger
class User(db.Model):
    __tablename__ = "user"
    user_id = db.Column(db.INTEGER,primary_key=True)
    #basic part:
    user_email = db.Column(db.String(255),nullable=False)
    user_password = db.Column(db.String(255),nullable=False)
    #information part
    user_name = db.Column(db.String(255))
    user_other_info = db.Column(db.String(2047))
    #security
    user_activate = db.Column(db.Boolean, default=False, nullable=False)
    user_last_token = db.Column(db.String(255),nullable=True)
    user_last_activate_time = db.Column(db.DateTime,nullable=True)
    user_top_secrect = db.Column(db.String(255),nullable=False)

class Embedder_Record(db.Model):
    __tablename__ = "embedderRecord"
    embedder_id = db.Column(db.INTEGER,primary_key=True)
    user_id = db.Column(db.INTEGER,db.ForeignKey("user.user_id"))
    user = db.relationship('User',backref=db.backref('embedder_records'))
    given_name = db.Column(db.String(255))
    activate_time = db.Column(db.DateTime,nullable=True)
    model_path = db.Column(db.String(255))
    file_path = db.Column(db.String(255))

class Audio_Record(db.Model):
    __tablename__ = "audioRecord"
    audio_id = db.Column(db.INTEGER,primary_key=True)
    activate_time = db.Column(db.DateTime,nullable=True)
    user_name = db.Column(db.String(255))
    file_path = db.Column(db.String(255))


def create_user(user_infor):
    user = User.query.filter_by(user_email=user_infor["email"]).first()
    if user:
        return False
    # customer_id = create_a_new_customer(user_infor)
    new_user = User()
    new_user.user_email = user_infor["email"]
    new_user.user_password = user_infor["password"]
    new_user.user_activate = True
    new_user.user_top_secrect = "111"
    db.session.add(new_user)
    db.session.commit()
    return True

def create_embedder_record(user,name,file_path):
    record = Embedder_Record()
    record.activate_time = datetime.now()
    record.user_id = user.user_id
    record.given_name = name
    record.file_path = file_path
    db.session.add(record)
    db.session.commit()
    return record.embedder_id

def create_audio_record(file_path,username=None):
    record = Audio_Record()
    record.activate_time = datetime.now()
    record.file_path = file_path
    if username:
        record.user_name = username
    db.session.add(record)
    db.session.commit()
    return record.audio_id

def Update_database():
    try:
        db.session.commit()
        # db.session.closed()
    except:
        logger.error("update database failed")
        db.session.rollback()

if __name__ == "__main__":
    db.create_all()