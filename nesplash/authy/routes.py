from flask import Blueprint, render_template, jsonify, request, session, current_app
from nesplash.authy.utils import (
    get_qrcode,
    get_registration_jwt,
    get_registration_status, 
    delete_authy_user,
    verify_authy_token
) 
from nesplash.decorator import login_required
from nesplash.models import User, Authy
from nesplash.extensions import db
from nesplash.ma import authySchema, userSchema

authy_bp = Blueprint("authy", __name__)

@authy_bp.route("/2fa/check")
@login_required
def twofa_token(*args, **kwargs):
    return render_template("account/authy/check_2fa.html")

@authy_bp.route("/2fa/enable")
@login_required
def twofa_enable(*args, **kwargs):
    return render_template("account/authy/enable_2fa.html")

@authy_bp.route("/2fa/qrcode/enable")
@login_required
def twofa_qrcode(*args, **kwargs):
    return render_template("account/authy/enable_2fa_qr.html")

@authy_bp.route("/api/user/2fa/enable", methods=['GET', 'POST'])
@login_required
def enable_2fa(*args, **kwargs):
    if request.method == 'POST':
        user = User.query.filter_by(email=kwargs["email"]).first()
        if user is None:
            return jsonify({"error": "none exist user"}), 400
        jwt = get_registration_jwt(user.id)
        session["registration_jwt"] = jwt
        return jsonify({"ok": True})
    return jsonify({"message": "transfer to enable 2fa html"})


@authy_bp.route("/api/user/2fa/enable/qrcode")
@login_required
def enable_2fa_qrcode(*args, **kwargs):
    jwt = session.get("registration_jwt")
    if not jwt:
        return jsonify({"error": "session jwt error"})
    return get_qrcode(jwt), 200, {
        'Content-Type': 'image/svg+xml',
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0'}


@authy_bp.route('/api/user/2fa/enable/poll')
@login_required
def enable_2fa_poll(*args, **kwargs):
    user = User.query.filter_by(email=kwargs["email"]).first()
    registration = get_registration_status(user.id)
    if registration['status'] == 'completed':
        del session["registration_jwt"]
        authy = Authy(
            user_id=user.id,
            authy_id=registration["authy_id"]
        )
        user.useAuthy = True
        db.session.add(authy)
        db.session.commit()
    elif registration['status'] != 'pending':
        return jsonify({"error": "an error has occured. please try again."})
    return jsonify({"message": registration['status']})


@authy_bp.route("/api/user/2fa/disable")
@login_required
def disable_2fa(*args, **kwargs):
    user = User.query.filter_by(email=kwargs["email"]).first()
    authy = authySchema.dump(user.authys)
    deleteConclusion = delete_authy_user(authy[0]["authy_id"])
    if deleteConclusion:
        authy = Authy.query.filter_by(user_id=user.id).first()
        db.session.delete(authy)
        user.useAuthy = False
        db.session.commit()
        return jsonify({"ok": True})
    else:
        return jsonify({"error": "An error has occurred. Please try again."})


@authy_bp.route("/api/user/2fa/check/token", methods=['POST'])
@login_required
def check_2fa_token(*args, **kwargs):
    token = request.json["token"]
    if token is None:
        return jsonify({"error": "none exist token"}), 400

    user = User.query.filter_by(email=kwargs["email"]).first()
    if user == None:
        return jsonify({"error": "none exist user"}), 400
    
    authy = authySchema.dump(user.authys)
    verification = verify_authy_token(authy[0]["authy_id"], token)
    message = verification.ok()
    if message:
        return jsonify({"ok": True})
    else:
        return jsonify({"error": "Token is invalid"})
