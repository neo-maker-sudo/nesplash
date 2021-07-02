import json
import os
from sqlalchemy.exc import IntegrityError
from nesplash.models import User, Photo, Category, Video, Method
from nesplash.extensions import db


def create_admin():
    user = User(
        username="zhangneo",
        email="eyywqkgb@gmail.com",
        bio="Hello, I am neo",
        location="Taiwan",
        profile_image="https://dkn8b9qqzonkk.cloudfront.net/profile_pics/default.jpg",
        link="www.neohub.cloud",
        methods=Method.query.filter_by(name="normal").first()
    )
    user.set_password("123456")
    db.session.add(user)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        
def create_architecture():
    with open((os.getcwd() + "/filter/topic_filter/architecture_filter.json"), "r", encoding="utf-8") as file:
        results = json.load(file)

    for result in results:
        user = User(
            username=result["username"],
            email=result["email"],
            password=result["password"],
            bio=result["bio"],
            location=result["location"],
            profile_image=result["profile_image"],
            total_collections=result["total_collections"],
            total_photos=result["total_photos"],
            link=result["website"],
            methods=Method.query.filter_by(name="normal").first()
        )
        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()

    for result in results:
        for image in result["images"]:
            photo = Photo(
                imageurl=image["imageUrl"],
                description=image["alt_description"],
                download=image["download"],
                author=User.query.filter_by(username=result["username"]).first(),
                categorys=Category.query.filter_by(name=image["category"]).first()
            )
            db.session.add(photo)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

def create_athletics():
    with open((os.getcwd() + "/filter/topic_filter/athletics_filter.json"), "r", encoding="utf-8") as file:
        results = json.load(file)

    for result in results:
        user = User(
            username=result["username"],
            email=result["email"],
            password=result["password"],
            bio=result["bio"],
            location=result["location"],
            profile_image=result["profile_image"],
            total_collections=result["total_collections"],
            total_photos=result["total_photos"],
            link=result["website"],
            methods=Method.query.filter_by(name="normal").first()
        )
        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()

    for result in results:
        for image in result["images"]:
            photo = Photo(
                imageurl=image["imageUrl"],
                description=image["alt_description"],
                download=image["download"],
                author=User.query.filter_by(username=result["username"]).first(),
                categorys=Category.query.filter_by(name=image["category"]).first()
            )
            db.session.add(photo)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

def create_food_drink():
    with open((os.getcwd() + "/filter/topic_filter/food_drink_filter.json"), "r", encoding="utf-8") as file:
        results = json.load(file)

    for result in results:
        user = User(
            username=result["username"],
            email=result["email"],
            password=result["password"],
            bio=result["bio"],
            location=result["location"],
            profile_image=result["profile_image"],
            total_collections=result["total_collections"],
            total_photos=result["total_photos"],
            link=result["website"],
            methods=Method.query.filter_by(name="normal").first()
        )
        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()

    for result in results:
        for image in result["images"]:
            photo = Photo(
                imageurl=image["imageUrl"],
                description=image["alt_description"],
                download=image["download"],
                author=User.query.filter_by(username=result["username"]).first(),
                categorys=Category.query.filter_by(name=image["category"]).first()
            )
            db.session.add(photo)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

def create_nature():
    with open((os.getcwd() + "/filter/topic_filter/nature_filter.json"), mode="r", encoding="utf-8") as file:
        results = json.load(file)

    for result in results:
        user = User(
            username=result["username"],
            email=result["email"],
            password=result["password"],
            bio=result["bio"],
            location=result["location"],
            profile_image=result["profile_image"],
            total_collections=result["total_collections"],
            total_photos=result["total_photos"],
            link=result["website"],
            methods=Method.query.filter_by(name="normal").first()
        )
        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()

    for result in results:
        for image in result["images"]:
            photo = Photo(
                imageurl=image["imageUrl"],
                description=image["alt_description"],
                download=image["download"],
                author=User.query.filter_by(username=result["username"]).first(),
                categorys=Category.query.filter_by(name=image["category"]).first()
            )
            db.session.add(photo)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

def create_people():
    with open((os.getcwd() + "/filter/topic_filter/people_filter.json"), mode="r", encoding="utf-8") as file:
        results = json.load(file)

    for result in results:
        user = User(
            username=result["username"],
            email=result["email"],
            password=result["password"],
            bio=result["bio"],
            location=result["location"],
            profile_image=result["profile_image"],
            total_collections=result["total_collections"],
            total_photos=result["total_photos"],
            link=result["website"],
            methods=Method.query.filter_by(name="normal").first()
        )
        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()

    for result in results:
        for image in result["images"]:
            photo = Photo(
                imageurl=image["imageUrl"],
                description=image["alt_description"],
                download=image["download"],
                author=User.query.filter_by(username=result["username"]).first(),
                categorys=Category.query.filter_by(name=image["category"]).first()
            )
            db.session.add(photo)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

def create_travel():
    with open((os.getcwd() + "/filter/topic_filter/travel_filter.json"), mode="r", encoding="utf-8") as file:
        results = json.load(file)

    for result in results:
        user = User(
            username=result["username"],
            email=result["email"],
            password=result["password"],
            bio=result["bio"],
            location=result["location"],
            profile_image=result["profile_image"],
            total_collections=result["total_collections"],
            total_photos=result["total_photos"],
            link=result["website"],
            methods=Method.query.filter_by(name="normal").first()
        )
        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()

    for result in results:
        for image in result["images"]:
            photo = Photo(
                imageurl=image["imageUrl"],
                description=image["alt_description"],
                download=image["download"],
                author=User.query.filter_by(username=result["username"]).first(),
                categorys=Category.query.filter_by(name=image["category"]).first()
            )
            db.session.add(photo)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

def create_contributor():
    with open((os.getcwd() + "/filter/contributor_filter/contributor_profile_filter.json"), "r", encoding="utf-8") as file:
        results = json.load(file)

        for result in results:
            user = User(
                username=result["username"],
                email=result["email"],
                password=result["password"],
                bio=result["bio"],
                location=result["location"],
                profile_image=result["profile_image"],
                total_collections=result["total_collections"],
                total_photos=result["total_photos"],
                link=result["website"],
                methods=Method.query.filter_by(name="normal").first()
            )
            db.session.add(user)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

def create_contributor_photos():
    with open((os.getcwd() + "/filter/contributor_filter/contributor_profile_filter.json"), "r", encoding="utf-8") as file:
        results = json.load(file)

        for result in results:
            for imageDT in result["images"]:
                photo = Photo(
                    imageurl=imageDT["imageUrl"],
                    description=imageDT["alt_description"],
                    download=imageDT["download"],
                    author=User.query.filter_by(username=result["username"]).first(),
                    categorys=Category.query.filter_by(name=imageDT["category"]).first()
                )
                db.session.add(photo)
                db.session.commit()

def create_architecture_video():
    with open(os.getcwd() + "/filter/topic_video/architecture_videos.json", "r", encoding="utf-8") as file:
        results = json.load(file)
        
        for result in results:
            video = Video(
                name=result["name"],
                videourl=result["videoUrl"],
                link=result["website"],
                categoryVideos=Category.query.filter_by(name=result["category"]).first()
            )
            db.session.add(video)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

def create_athletics_video():
    with open(os.getcwd() + "/filter/topic_video/athletics_videos.json", "r", encoding="utf-8") as file:
        results = json.load(file)

        for result in results:
            video = Video(
                name=result["name"],
                videourl=result["videoUrl"],
                link=result["website"],
                categoryVideos=Category.query.filter_by(name=result["category"]).first()
            )
            db.session.add(video)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

def create_food_drink_video():
    with open(os.getcwd() + "/filter/topic_video/food_drink_videos.json", "r", encoding="utf-8") as file:
        results = json.load(file)

        for result in results:
            video = Video(
                name=result["name"],
                videourl=result["videoUrl"],
                link=result["website"],
                categoryVideos=Category.query.filter_by(name=result["category"]).first()
            )
            db.session.add(video)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

def create_nature_video():
    with open(os.getcwd() + "/filter/topic_video/nature_videos.json", "r", encoding="utf-8") as file:
        results = json.load(file)

        for result in results:
            video = Video(
                name=result["name"],
                videourl=result["videoUrl"],
                link=result["website"],
                categoryVideos=Category.query.filter_by(
                    name=result["category"]).first()
            )
            db.session.add(video)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

def create_people_video():
    with open(os.getcwd() + "/filter/topic_video/people_videos.json", "r", encoding="utf-8") as file:
        results = json.load(file)

        for result in results:
            video = Video(
                name=result["name"],
                videourl=result["videoUrl"],
                link=result["website"],
                categoryVideos=Category.query.filter_by(name=result["category"]).first()
            )
            db.session.add(video)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

def create_travel_video():
    with open(os.getcwd() + "/filter/topic_video/travel_videos.json", "r", encoding="utf-8") as file:
        results = json.load(file)

        for result in results:
            video = Video(
                name=result["name"],
                videourl=result["videoUrl"],
                link=result["website"],
                categoryVideos=Category.query.filter_by(name=result["category"]).first()
            )
            db.session.add(video)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
