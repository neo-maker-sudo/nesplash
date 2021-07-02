from flask import Blueprint, render_template, request, jsonify
from nesplash.models import Photo, Video, User
from nesplash.ma import photoSchema, videoSchema, userSchema


nature_bp = Blueprint("nature", __name__)


@nature_bp.route('/nature/main')
def index():
    return render_template('category/nature/index.html')

@nature_bp.route("/nature/video")
def video():
    return render_template('category/nature/video.html')

@nature_bp.route("/nature/contributor")
def contributor():
    return render_template('category/nature/contributor.html')

@nature_bp.route("/nature/api/photos")
def nature_mainpage():
    page = request.args.get("page", None)
    arr = []
    query = Photo.query.filter_by(category_id=4).order_by(Photo.id.desc()).offset(int(page)*12).limit(12)
    results = photoSchema.dump(query)
    if results != []:
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

        if len(arr) < 12:
            return jsonify({"nextPage": None, "message": arr})
        else:
            query_data_check = Photo.query.filter_by(category_id=4).order_by(Photo.id.desc()).offset((int(page)+1)*12).limit(12)
            results_check = photoSchema.dump(query_data_check)
            if results_check != []:
                return jsonify({"message": arr, "nextPage": int(page) + 1})
            else:
                return jsonify({"nextPage": None, "message": arr})
    else:
        return jsonify({"nextPage": None, "message": []})

@nature_bp.route("/nature/api/videos")
def nature_videos():
    page = request.args.get("page", None)
    query = Video.query.filter_by(category_id=4).order_by(Video.id.asc()).offset(int(page)*12).limit(12)
    results = videoSchema.dump(query)
    if results != []:
        if len(results) < 12:
            return jsonify({"nextPage": None, "message": results})
        else:
            query_data_check = Video.query.filter_by(category_id=4).order_by(Video.id.asc()).offset((int(page)+1)*12).limit(12)
            results_check = videoSchema.dump(query_data_check)
            if results_check != []:
                return jsonify({"nextPage": int(page) + 1, "message": results})
            else:
                return jsonify({"NextPage": None, "message": results})
    else:
        return jsonify({"NextPage": None, "message": []})

@nature_bp.route("/nature/api/contributor")
def nature_contributor():
    page = request.args.get("page", None)
    user = User.query.join(Photo).filter_by(category_id=4).group_by(User.username).order_by(User.total_photos.desc()).offset(int(page)*12).limit(12)
    results = userSchema.dump(user)
    if results != []:
        if len(results) < 12:
            return jsonify({"nextPage": None, "message": results})
        else:
            query_data_check = User.query.join(Photo).filter_by(category_id=4).group_by(User.username).order_by(User.total_photos.desc()).offset((int(page)+1)*12).limit(12)
            results_check = userSchema.dump(query_data_check)
            if results_check != []:
                return jsonify({"nextPage": int(page) + 1, "message": results})
            else:
                return jsonify({"NextPage": None, "message": results})
    else:
        return jsonify({"NextPage": None, "message": []})
