import secrets
import os
import boto3
from werkzeug.utils import secure_filename
from PIL import Image
from flask import url_for, current_app
from threading import Thread
from flask_mail import Message
from nesplash.extensions import mail

s3 = boto3.client('s3',
                    aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
                    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
                    )

s3_resource = boto3.resource('s3',
                            aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
                            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
                            )

bucket = "message-board-pratice"

def send_register_mail(user):
    token = user.get_reset_token()
    message = Message("SIGNUP REGISTER CONFIRM MAIL", sender="noreply@demo.com", recipients=[user.email])
    message.body = f"""
    confirm email to grant your personal nesplash function
    {url_for("user.confirm_email", token=token, _external=True)}
    If you did not make this request, then just ignore this email and no change anything
    """
    app = current_app._get_current_object()
    thr = Thread(target=_async_send_mail, args=[app, message])
    thr.start()
    return thr


def send_change_password_mail(user):
    token = user.get_reset_token()
    message = Message("Reset Password", sender="noreply@demo.com", recipients=[user.email])
    message.body = f"""
    to reset your password, visiting below link : 
    {url_for("user.reset_password", token=token, _external=True)}
    If you did not make this request, then just ignore this email and no change anything
    """
    app = current_app._get_current_object()
    thr = Thread(target=_async_send_mail, args=[app, message])
    thr.start()
    return thr


def _async_send_mail(app, message):
    with app.app_context():
        mail.send(message)


def s3_profile_pics(picture):
    random_hex = secrets.token_hex(8)
    _, _ext = os.path.splitext(picture.filename)
    pic_filename = random_hex + _ext
    pic_path = os.path.join(current_app.root_path,'static/profile_pics', pic_filename)

    output_size = (125, 125)
    i = Image.open(picture)
    if i.mode == "P":
        i = i.convert('RGB')
    i.thumbnail(output_size)
    i.save(pic_path)

    key_path = "profile_pics/" + pic_filename
    s3.upload_file(Bucket=bucket, Filename=pic_path, Key=key_path)
    
    return pic_filename


def s3_public_pics(picture):
    random_hex = secrets.token_hex(8)
    _, _ext = os.path.splitext(picture.filename)
    pic_filename = random_hex + _ext
    pic_path = os.path.join(current_app.root_path,'static/public_pics', pic_filename)

    filename = secure_filename(pic_filename)
    picture.save(pic_path)
    key_path = "public_pics/" + pic_filename
    
    thr = Thread(s3.upload_file(Bucket=bucket, Filename=pic_path, Key=key_path))
    thr.start()
    
    return pic_filename


def obj_last_modified(myobj):
    return myobj.last_modified
