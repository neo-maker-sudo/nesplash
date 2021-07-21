import secrets
import os
import boto3
import time
from werkzeug.utils import secure_filename
from PIL import Image
from flask import url_for, current_app
from threading import Thread
from flask_mail import Message
from nesplash.extensions import mail, model

from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from keras.applications.vgg16 import preprocess_input
from keras.applications.vgg16 import decode_predictions
import numpy as np

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
    {url_for("user.confirm_email", token=token, _external=True, _scheme="https")}
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
    {url_for("user.reset_password", token=token, _external=True, _scheme="https")}
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


    basewidth = 320
    i = Image.open(picture)
    if i.mode == "P":
        i = i.convert("RGB")
    wpercent = (basewidth/float(i.size[0]))
    hsize = int((float(i.size[1])*float(wpercent)))
    i = i.resize((basewidth, hsize), Image.ANTIALIAS)
    i.save(pic_path)

    key_path = "public_pics/" + pic_filename
    labelName = keras_model(pic_path)
    thr = Thread(s3.upload_file(Bucket=bucket, Filename=pic_path, Key=key_path))
    thr.start()
    
    return pic_filename, labelName


def obj_last_modified(myobj):
    return myobj.last_modified


def keras_model(img_path):
    image = load_img(img_path, target_size=(224, 224))
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)
    image = preprocess_input(image)
    result = model.predict(image)
    
    # label 第一次出來會有五個預測內容 
    # [
    #     [
    #         ('n03724870', 'mask', 0.10736913), 
    #         ('n03866082', 'overskirt', 0.09860326),
    #         ('n03958227', 'plastic_bag', 0.096884824), 
    #         ('n03534580', 'hoopskirt', 0.07662964),
    #         ('n07836838', 'chocolate_sauce', 0.06463431)
    #     ]
    # ]
    label = decode_predictions(result)

    # 取出label最高機率的內容
    label = label[0][0]
    
    # 最終結果，並加入字串與轉換為百分比 Ex : mask (10.74%)
    classification = '%s (%.2f%%)' % (label[1], label[2]*100)

    return classification


