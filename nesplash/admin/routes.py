from flask import Blueprint, render_template, jsonify, request
from nesplash.decorator import login_required, admin_required
from nesplash.models import User, Photo
from nesplash.ma import userSchema, photoSchema
from nesplash.user.util import send_change_password_mail, send_register_mail
from nesplash.extensions import db


admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/admin")
@login_required
@admin_required("ADMINISTER")
def admin_users_page(*args, **kwargs):
    return render_template("admin/users.html")

@admin_bp.route("/admin/photos")
@login_required
@admin_required("ADMINISTER")
def admin_photos_page(*args, **kwargs):
    return render_template("admin/photos.html")

@admin_bp.route("/admin/users")
@login_required
@admin_required("ADMINISTER")
def admin_user_data(*args, **kwargs):
    users = User.query.all()
    results = userSchema.dump(users)
    return jsonify({"ok": True, "message": results}) 

@admin_bp.route("/api/admin/help-resend-mail", methods=['POST'])
@login_required
@admin_required("ADMINISTER")
def admin_help_user_send_forgetEmail(*args, **kwargs):
    if request.method == "POST":
        user_id = request.json["id"]

        user = User.query.get(user_id)
        if user:
            send_change_password_mail(user)
            return jsonify({"ok": True})
        else:
            return jsonify({"error": "none exist user"})

@admin_bp.route("/api/admin/lock-authority", methods=['POST'])
@login_required
@admin_required("ADMINISTER")
def admin_lower_authority(*args, **kwargs):
    if request.method == "POST":
        user_id = request.json["id"]

        user = User.query.get(user_id)

        if user is None:
            return jsonify({"error": "none exist user"})
        
        user.locked()
        
        return jsonify({"ok": True})

@admin_bp.route("/api/admin/help-resend-confirm-mail", methods=['POST'])
@login_required
def admn_help_user_send_confirmEmail(*args, **kwargs):
    user_id = request.json["id"]
    user = User.query.get(user_id)
    if user:
        send_register_mail(user)
        return jsonify({"ok": True})
    else:
        return ({"error": "none exist user"})
@admin_bp.route("/api/admin/unlock-authority", methods=['POST'])
@login_required
@admin_required("ADMINISTER")
def admin_recover_authority(*args, **kwargs):
    if request.method == "POST":
        user_id = request.json["id"]

        user = User.query.get(user_id)

        if user is None:
            return jsonify({"error": "none exist user"})

        user.unlocked()

        return jsonify({"ok": True})

@admin_bp.route("/api/admin/users-data", methods=['POST'])
@login_required
@admin_required("ADMINISTER")
def admin_specific_user_data(*args, **kwargs):
    if request.method == 'POST':
        username =request.json["username"]
        users = User.query.whooshee_search(username)
        results = userSchema.dump(users)
        return jsonify({"ok": True, "message": results})


@admin_bp.route("/api/admin/photos-data", methods=['POST'])
@login_required
@admin_required("ADMINISTER")
def admin_photo_data(*args, **kwargs):
    if request.method == 'POST': 
        photo_id = request.json["photo_id"]   
        photo = Photo.query.get(photo_id)

        if photo is None:
            return jsonify({"error": "none exist photo"})
        data = {
            "id": photo.id,
            "imageurl": photo.imageurl,
            "username": photo.author.username,
            "user_id": photo.author.id
        }
        return jsonify({"ok": True, "message": data})

@admin_bp.route("/api/admin/delete/photos-data", methods=['DELETE'])
@login_required
@admin_required("ADMINISTER")
def admin_delete_photo_data(*args, **kwargs):
    if request.method == 'DELETE':
        photo_id = request.json["photo_id"]
        photo = Photo.query.get(photo_id)

        if photo is None:
            return jsonify({"error": "none exist photo"})

        db.session.delete(photo)
        db.session.commit()
        return jsonify({"ok": True})
