from flask import Blueprint, request, current_app, render_template, jsonify, session, abort
from nesplash.models import Photo, User, Collection
from nesplash.ma import photoSchema, collectionSchema
from nesplash.decorator import login_required


main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    return render_template("main.html")

@main_bp.route("/api/photos")
def photos():
    page = request.args.get("page", None)
    arr = []
    query = Photo.query.order_by(Photo.id.desc()).offset(int(page)*12).limit(12)
    results = photoSchema.dump(query)

    for result in results:
        photo = Photo.query.get_or_404(result["id"])
        data = {
            "id": result["id"],
            "imageurl": result["imageurl"],
            "description": result["description"],
            "download": result["download"],
            "user": photo.author.username,
            "link": photo.author.link,
            "profile_image": photo.author.profile_image,
            "user_id": photo.author.id
        }
        arr.append(data)
    if results != []:
        if len(results) < 12:
            return jsonify({"nextPage": None, "message": arr})
        else:
            query_data_check = query = Photo.query.order_by(Photo.id.desc()).offset(int(page)*12).limit(12)
            results_check = photoSchema.dump(query_data_check)
            if results_check != []:
                return jsonify({"nextPage": int(page) + 1, "message": arr})
            else:
                return jsonify({"nextPage": None, "message": arr})
    else:
        return jsonify({"nextPage": None, "message": []})


@main_bp.route("/api/photos/search")
def search_photos():
    keyword = request.args.get("q", None)
    page = request.args.get("page", None)

    arr = []
    photos = Photo.query.filter(Photo.description.like(f"%%{keyword}%%")).order_by(Photo.timestamp.desc()).offset(int(page)*12).limit(12)
    results = photoSchema.dump(photos)
    for result in results:
        photo = Photo.query.get_or_404(result["id"])
        data = {
            "id": result["id"],
            "imageurl": result["imageurl"],
            "description": result["description"],
            "download": result["download"],
            "user": photo.author.username,
            "link": photo.author.link,
            "profile_image": photo.author.profile_image,
            "user_id": photo.author.id
        }
        arr.append(data)

    if len(results) < 12:
        return jsonify({"nextPage": None, "message": arr})
    else:
        photos_check = Photo.query.filter(Photo.description.like(f"%%{keyword}%%")).order_by(Photo.timestamp.desc()).offset((int(page)+1)*12).limit(12)
        check_data = photoSchema.dump(photos_check)
        if check_data != []:
            return jsonify({"nextPage": int(page) +1, "message": arr})
        else:
            return jsonify({"nextPage": None, "message": arr})

@main_bp.route("/api/collected_photo_id")
def collected_photo_id():
    arr = []
    sess = session.get("email")
    if sess:
        user = User.query.filter_by(email=sess).first()
        collects = Collection.query.with_parent(user).order_by(Collection.collected_id.asc()).all()
        results = collectionSchema.dump(collects)
        for result in results:
            arr.append(result["collected_id"])
        return jsonify({"message": arr})
    return jsonify({"message": []})
