from flask import Blueprint, render_template, request, jsonify
from nesplash.models import Photo, User, Video
from nesplash.ma import photoSchema, videoSchema, userSchema


travel_bp = Blueprint("travel", __name__)


@travel_bp.route('/travel/main')
def index():
    return render_template('category/travel/index.html')

@travel_bp.route("/travel/video")
def video():
    return render_template('category/travel/video.html')

@travel_bp.route("/travel/contributor")
def contributor():
    return render_template('category/travel/contributor.html')

@travel_bp.route("/travel/api/photos")
def travel_mainpage():
    page = request.args.get("page", None)
    arr = []
    query = Photo.query.filter_by(category_id=6).order_by(Photo.id.desc()).offset(int(page)*12).limit(12)
    results = photoSchema.dump(query)
    if results != []:
        for result in results:
            photo = Photo.query.get_or_404(result["id"])
            data = {
                "id": result["id"],
                "imageUrl": result["imageUrl"],
                "description": result["description"],
                "download": result["download"],
                "user": photo.author.username,
                "link": photo.author.link,
                "profile_image": photo.author.profile_image,
                "user_id": photo.author.id
            }
            arr.append(data)

        if len(arr) < 12:
            return jsonify({"nextPage": None, "message": arr})
        else:
            query_data_check = Photo.query.filter_by(category_id=6).order_by(Photo.id.desc()).offset((int(page)+1)*12).limit(12)
            results_check = photoSchema.dump(query_data_check)
            if results_check != []:
                return jsonify({"message": arr, "nextPage": int(page) + 1})
            else:
                return jsonify({"nextPage": None, "message": arr})
    else:
        return jsonify({"nextPage": None, "message": []})

@travel_bp.route("/travel/api/videos")
def travel_videos():
    page = request.args.get("page", None)
    query = Video.query.filter_by(category_id=6).order_by(Video.id.asc()).offset(int(page)*12).limit(12)
    results = videoSchema.dump(query)
    if results != []:
        if len(results) < 12:
            return jsonify({"nextPage": None, "message": results})
        else:
            query_data_check = Video.query.filter_by(category_id=6).order_by(Video.id.asc()).offset((int(page)+1)*12).limit(12)
            results_check = videoSchema.dump(query_data_check)
            if results_check != []:
                return jsonify({"nextPage": int(page) + 1, "message": results})
            else:
                return jsonify({"NextPage": None, "message": results})
    else:
        return jsonify({"NextPage": None, "message": []})

@travel_bp.route("/travel/api/contributor")
def travel_contributor():
    page = request.args.get("page", None)
    user = User.query.join(Photo).filter_by(category_id=6).group_by(User.username).order_by(User.total_photos.desc()).offset(int(page)*12).limit(12)
    results = userSchema.dump(user)
    if results != []:
        if len(results) < 12:
            return jsonify({"nextPage": None, "message": results})
        else:
            query_data_check = User.query.join(Photo).filter_by(category_id=6).group_by(User.username).order_by(User.total_photos.desc()).offset((int(page)+1)*12).limit(12)
            results_check = userSchema.dump(query_data_check)
            if results_check != []:
                return jsonify({"nextPage": int(page) + 1, "message": results})
            else:
                return jsonify({"NextPage": None, "message": results})
    else:
        return jsonify({"NextPage": None, "message": []})
