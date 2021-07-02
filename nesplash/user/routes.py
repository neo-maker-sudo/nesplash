from flask import Blueprint, render_template, session, request, jsonify, redirect, url_for
from nesplash.models import User, Photo, Collection, Follow, Category, Method
from nesplash.extensions import db
from nesplash.decorator import login_required
from nesplash.user.util import send_register_mail, send_change_password_mail, s3_profile_pics, s3_public_pics
from nesplash.ma import userSchema, photoSchema, collectionSchema, followSchema
from werkzeug.security import check_password_hash

import time

user_bp = Blueprint("user", __name__)


# signin and signup routes
@user_bp.route("/signup")
def signup():
    return render_template("signup.html")

@user_bp.route("/signin")
def signin():
    return render_template("signin.html")

@user_bp.route("/api/user", methods=['GET', 'POST', 'PATCH', 'DELETE'])
def member():
    # 註冊
    if request.method == "POST":
        username = request.json["username"]
        email = request.json["email"].lower()
        password = request.json["password"]
    
        email_check = User.query.filter_by(email=email).first()
        
        if email_check:
            return jsonify({"error": True, "message": "email has already been taken, please use another one"})

        username_check = User.query.filter_by(username=username).first()
        
        if username_check is not None:
            if username_check.username == username:
                return jsonify({"error": True, "message": "duplicate username"})

        user = User(
            username=username, 
            email=email,
            methods=Method.query.filter_by(name="normal").first()
        )
        user.set_password(password)
        send_register_mail(user)
        db.session.add(user)
        db.session.commit()
        return jsonify({"ok": True}), 201
    # 登入
    elif request.method == "PATCH":
        email = request.json["email"]
        password = request.json["password"]
        user = User.query.filter_by(email=email).first()
        if user is None:
            return jsonify({"error": True, "message": "none exist user"}), 400
        else:
            if user.validate_password(password):
                session["email"] = user.email
                return jsonify({"ok": True}), 201
            else:
                return jsonify({"error": True, "message": "wrong password"}), 401
    # 登出
    elif request.method == "DELETE":
        session.pop("email")
        return jsonify({"ok": True})
    else:
        sess = session.get("email")
        if sess:
            user = User.query.filter_by(email=sess).first()
            return jsonify({"message": {
                "id": user.id,
                "email": user.email,
                "username": user.username,
                "role_id": user.role_id,
                "lock_status": user.lock_status
            }})
        else:
            return jsonify({"message": None}), 403


# reset change routes
@user_bp.route("/api/user/reset-page", methods=['GET', 'POST'])
def reset_page():
    if request.method == "POST":
        email =request.json["email"]

        if email == "":
            return jsonify({"error": True, "message": "email must not be empty"}), 400

        user = User.query.filter_by(email=email).first()
        if user:
            send_change_password_mail(user)
            return jsonify({"ok": True})
        else:
            return jsonify({"error": "none exist user"}), 400

    return render_template("reset_request.html")

@user_bp.route("/api/user/reset-password/<token>", methods=['GET', 'POST'])
def reset_password(token):
    if request.method == "POST":
        password = request.json["password"]
        conform_password = request.json["conform_password"]

        if not password == conform_password:
            return jsonify({"error": True, "message": "password and conform_password not same"}), 400

        user = User.validate_token(token)
        
        if user is None:
            return jsonify({"error": True, "message": "Invalid or expired token"}), 400
        else:
            user.set_password(password)
            db.session.commit()
            return jsonify({"ok": True})
        
    return render_template("reset_password.html")

@user_bp.route("/api/user/change-password/<int:user_id>", methods=['POST'])
def change_password(user_id):
    user = User.query.get_or_404(user_id)

    if user is None:
        return jsonify({"error": "none exist user"}), 400

    if request.method == "POST":
        password = request.json["password"]
        conform_password = request.json["conform_password"]

        if not password == conform_password:
            return jsonify({"error": True, "message": "password and conform_password not same"}), 400
        
        user.set_password(password)
        db.session.commit()
        return jsonify({"ok": True})


# confirm routes
@user_bp.route("/api/user/confirm/<token>")
def confirm_email(token):
    return render_template("account/confirm.html")

@user_bp.route("/api/user/confirm-email", methods=['POST'])
def confirm_signUpToken():
    if request.method == 'POST':
        token = request.json["token"]

        user = User.validate_token(token)

        if user is None:
            return jsonify({"error": True, "message": "Invalid or expired token"}), 400

        user.confirmed = 1
        db.session.commit()

        return jsonify({"ok": True, "message": user.username})


# public routess
@user_bp.route("/public/<int:id>")
def public_page(id):
    return render_template("public.html")

@user_bp.route("/api/public/<int:user_id>")
def public_page_api(user_id):
    page = request.args.get("page", None)
    user = User.query.get_or_404(user_id)
    photos = Photo.query.filter_by(author_id=user_id).order_by(Photo.id.asc()).offset(int(page)*12).limit(12)
    
    results = photoSchema.dump(photos)
    
    data = {
        "username": user.username,
        "link": user.link,
        "bio": user.bio,
        "location": user.location,
        "profile_image": user.profile_image,
        "total_collections": user.total_collections,
        "total_photos": user.total_photos
    }

    if results != []:
        if len(results) < 12:
            return jsonify({"nextPage": None, "message": results, "user": data})
        else:
            query_data_check = Photo.query.filter_by(author_id=user_id).order_by(Photo.id.asc()).offset(int(page)*12).limit(12)
            results_check = photoSchema.dump(query_data_check)
            if results_check != []:
                return jsonify({"nextPage": int(page) + 1, "message": results, "user": data})
            else:
                return jsonify({"NextPage": None, "message": results, "user": data})
    else:
        if data == []:
            return jsonify({"nextPage": None, "message": []})
        return jsonify({"nextPage": None, "user": data})


# account person and pictures routes
@user_bp.route("/account/upload_pictures")
@login_required
def upload_pictures_page():
    return render_template("account/upload_pictures_page.html")

@user_bp.route("/account/data")
@login_required
def person_data():
    return render_template("account/personData.html")

@user_bp.route("/api/account/data")
@login_required
def person_data_api():
    sess = session.get("email")
    if sess:
        current_user = User.query.filter_by(email=sess).first()
        return jsonify({"message": {
            "id": current_user.id,
            "email": current_user.email,
            "username": current_user.username,
            "location": current_user.location,
            "bio": current_user.bio,
            "profile_image": current_user.profile_image,
            "confirmed_status": current_user.confirmed,
            "lock_status": current_user.lock_status,
            "user_method": current_user.methods.name
        }})
    else:
        return jsonify({"message": []})

@user_bp.route("/api/user/change-bio/<int:user_id>", methods=['POST'])
@login_required
def change_bio(user_id):
    user = User.query.get_or_404(user_id)
    
    if user is None:
        return jsonify({"error": "none exist user"}), 400

    if request.method == "POST":
        bio = request.json["bio"]
        user.bio = bio
        db.session.commit()
        return jsonify({"ok": True})

@user_bp.route("/api/user/change-username/<int:user_id>", methods=['POST'])
@login_required
def change_username(user_id):
    user = User.query.get_or_404(user_id)

    if user is None:
        return jsonify({"error": "none exist user"}), 400

    if request.method == "POST":
        username = request.json["username"]

        duplicate = User.query.filter_by(username=username).first()
        if duplicate:
            return jsonify({"error": "username already be taken, change anthor one"}), 400
        else:
            user.username = username
            db.session.commit()
            return jsonify({"ok": True})

@user_bp.route("/api/user/change-location/<int:user_id>", methods=['POST'])
@login_required
def change_location(user_id):
    user = User.query.get_or_404(user_id)

    if user is None:
        return jsonify({"error": "none exist user"}), 400

    if request.method == "POST":
        location = request.json["location"]

        user.location = location
        db.session.commit()
        return jsonify({"ok": True})

@user_bp.route("/api/user/delete-account/<int:user_id>", methods=['DELETE'])
@login_required
def delete_account(user_id):
    user = User.query.get_or_404(user_id)

    if user is None:
        return jsonify({"error": "none exist user"}), 400

    if request.method == "DELETE":
        db.session.delete(user)
        db.session.commit()
        session.pop("email")
        return jsonify({"ok": True})

@user_bp.route("/api/user/upload-profile-image/<int:user_id>", methods=['POST'])
@login_required
def upload_profile_image(user_id):
    user = User.query.get_or_404(user_id)

    if user is None:
        return jsonify({"error": "none exist user"}), 400

    if request.method == "POST":
        file = request.files["file"]
        clean_fn = s3_profile_pics(file)

        user.profile_image = ("https://dkn8b9qqzonkk.cloudfront.net/profile_pics/" + clean_fn)
        db.session.commit()
        return jsonify({"ok": True, "message": clean_fn})

@user_bp.route("/api/user/upload-public-image/<int:user_id>", methods=['POST'])
@login_required
def upload_public_image(user_id):
    user = User.query.get_or_404(user_id)

    if user is None:
        return jsonify({"error": "none exist user"}), 400

    if request.method == "POST":
        file = request.files["file"]
        description = request.form["description"]
        category = request.form["category"]
        clean_fn = s3_public_pics(file)
        user.upload_public_photo(user, description, category, clean_fn)
        return jsonify({"ok": True})
    else:
        return jsonify({"message": []})

@user_bp.route("/api/user/delete-public-image", methods=['POST'])
@login_required
def delete_public_image():
    if request.method == 'POST':
        photo_id = request.json["id"]
        photo = Photo.query.get(photo_id)

        if photo is None:
            return jsonify({"error": "none exist photo"}), 400

        db.session.delete(photo)
        db.session.commit()
        return jsonify({"ok": True})

@user_bp.route("/api/user/personal-photos")
@login_required
def personal_photo_id():
    page = request.args.get("page", None)
    sess = session.get("email")
    if sess:
        user = User.query.filter_by(email=sess).first()
        photos = Photo.query.filter_by(author_id=user.id).offset(int(page)*12).limit(12)
        results = photoSchema.dump(photos)
        if len(results) < 12:
            return jsonify({"nextPage": None, "message": results})
        else:
            photos_check = Photo.query.filter_by(author_id=user.id).offset((int(page)+1)*12).limit(12)
            check_data = photoSchema.dump(photos_check)
            if check_data != []:
                return jsonify({"nextPage": int(page) + 1, "message": results})
            else:
                return jsonify({"nextPage": None, "message": results})
    return jsonify({"message": []})


# collection
@user_bp.route("/account/collections")
@login_required
def collections_page():
    return render_template("account/collections_page.html")

@user_bp.route("/api/user/collect-photos")
@login_required
def account_collections_page():
    arr = []
    page = request.args.get("page", None)
    sess = session.get("email")
    if sess:
        user = User.query.filter_by(email=sess).first()
        collects = Collection.query.with_parent(user).order_by(Collection.timestamp.asc()).offset(int(page)*12).limit(12)
        results = collectionSchema.dump(collects)
        
        for result in results:
            photo = Photo.query.get_or_404(result["collected_id"])
            data = {
                "id": photo.id,
                "imageurl": photo.imageurl,
                "description": photo.description,
                "download": photo.download,
                "user": photo.author.username,
                "link": photo.author.link,
                "profile_image": photo.author.profile_image,
                "timestamp": photo.timestamp,
                "user_id": photo.author.id
            }
            arr.append(data)

        if len(results) < 12:
            return jsonify({"nextPage": None, "message": arr})
        else:
            collects_check = Collection.query.with_parent(user).order_by(Collection.timestamp.asc()).offset((int(page)+1)*12).limit(12)
            check_data = collectionSchema.dump(collects_check)
            if check_data != []:
                return jsonify({"nextPage": int(page) + 1 , "message": arr})
            else:
                return jsonify({"nextPage": None, "message": arr})
    else:
        return jsonify({"message": []})

@user_bp.route("/api/collect/<int:photo_id>")
def collect_pics(photo_id):
    sess = session.get("email")
    if sess:
        user = User.query.filter_by(email=sess).first()
        photo = Photo.query.get_or_404(photo_id)

        if photo is None:
            return jsonify({"error": True, "message": "not exist photo"}), 400

        user.collect(photo)

        return jsonify({"ok": True})
    else:
        return jsonify({"error": "you have to login first"})

@user_bp.route("/api/uncollect/<int:photo_id>")
def uncollect_pics(photo_id):
    sess = session.get("email")
    if sess:
        user = User.query.filter_by(email=sess).first()
        photo = Photo.query.get_or_404(photo_id)

        if photo is None:
            return jsonify({"error": "not exist photo"}), 400

        user.uncollect(photo)

        return jsonify({"ok": True})
    else:
        return jsonify({"error": "you have to login first"})
        
# follow and unfollow routes
@user_bp.route("/account/following")
@login_required
def following_page():
    return render_template("account/following_page.html")

@user_bp.route("/account/followers")
@login_required
def followers_page():
    return render_template("account/followers_page.html")

@user_bp.route("/api/follow/<int:user_id>")
def follow(user_id):
    sess = session.get("email")
    if sess:
        
        current_user = User.query.filter_by(email=sess).first()
        followed_user = User.query.get_or_404(user_id)
        
        if followed_user is None:
            return jsonify({"error": "none exist user"}), 400

        current_user.follow(followed_user)

        return jsonify({"ok": True})
    else:
        return jsonify({"error":  "you have to login first"})

@user_bp.route("/api/unfollow/<int:user_id>")
def unfollow(user_id):
    sess = session.get("email")
    if sess:
        current_user = User.query.filter_by(email=sess).first()
        followed_user = User.query.get_or_404(user_id)
        
        if followed_user is None:
            return jsonify({"error": "none exist user"}), 400

        current_user.unfollow(followed_user)
        return jsonify({"ok": True})
    else:
        return jsonify({"error":  "you have to login first"})

@user_bp.route("/api/is_following_or_not/<int:user_id>")
@login_required
def follow_status(user_id):
    sess = session.get("email")
    if sess:
        current_user = User.query.filter_by(email=sess).first()
        user = User.query.get_or_404(user_id)
        result = current_user.is_following(user)
        if result:
            return jsonify({"message": "match"})
        else:
            return jsonify({"message": "nomatch"})
    else:
        return jsonify({"message": []})
    
@user_bp.route("/api/user/following")
@login_required
def account_following_page():
    arr = []
    page = request.args.get("page", None)
    sess = session.get("email")
    if sess:
        current_user = User.query.filter_by(email=sess).first()
        followed = Follow.query.filter_by(follower_id=current_user.id).order_by(Follow.followed_id.asc()).offset(int(page)*12).limit(12)
        results = followSchema.dump(followed)
        for result in results:
            if result["followed_id"] == current_user.id:
                continue
            user = User.query.get_or_404(result["followed_id"])
            data = {
                "id": user.id,
                "username": user.username,
                "link": user.link,
                "profile_image": user.profile_image
            }
            arr.append(data)
        if len(result) < 12:
            return jsonify({"nextPage": None, "message": arr})
        else:
            followed_check = Follow.query.filter_by(follower_id=current_user.id).order_by(Follow.followed_id.asc()).offset((int(page)+1)*12).limit(12)
            check_data = followSchema.dump(followed_check)
            if check_data != []:
                return jsonify({"nextPage": int(page) + 1,"message": arr})
            else:
                return jsonify({"nextPage": None, "message": arr})
    else:
        return jsonify({"message": []})

@user_bp.route("/api/user/followers")
@login_required
def account_followers_page():
    arr = []
    page = request.args.get("page", None)
    sess = session.get("email")
    if sess:
        current_user = User.query.filter_by(email=sess).first()
        followers = Follow.query.filter_by(followed_id=current_user.id).order_by(Follow.follower_id.asc()).offset(int(page)*12).limit(12)
        results = followSchema.dump(followers)

        for result in results:
            if result["follower_id"] == current_user.id:
                continue
            user = User.query.get_or_404(result["follower_id"])
            data = {
                "id": user.id,
                "username": user.username,
                "link": user.link,
                "profile_image": user.profile_image
            }
            arr.append(data)

        if len(results) < 12:
            return jsonify({"nextPage": None, "message": arr})
        else:
            followers_check = Follow.query.filter_by(followed_id=current_user.id).order_by(Follow.follower_id.asc()).offset((int(page)+1)*12).limit(12)
            check_data = followSchema.dump(followers_check)
            if check_data != []:
                return jsonify({"nextPage": int(page) + 1, "message": arr})
            else:
                return jsonify({"nextPage": None, "message": arr})
    else:
        return jsonify({"message": []})



