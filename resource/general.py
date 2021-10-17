from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from passlib.context import CryptContext
import configparser
security_config = configparser.ConfigParser()
security_config.read("config/general_config.conf")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
login_config = {
    "SECRET_KEY":security_config["security"]["SECRET_KEY"],
    "expiration": int(security_config["security"]["expiration"])
}
general_serializer = Serializer(login_config['SECRET_KEY'],
                       expires_in=login_config['expiration'])

email_config = security_config["emailcontent"]
reset_password_link = email_config["reset_password_link"]
activate_user_link = email_config["activate_user_link"]