from flask import current_app
from authy.api import AuthyApiClient
from io import BytesIO
import time
import qrcode
import qrcode.image.svg
import jwt


def get_registration_status(user_id):
    authy_api = AuthyApiClient(current_app.config["AUTHY_PRODUCTION_API_KEY"])
    resp = authy_api.users.registration_status(user_id)
    if not resp.ok():
        return {'status': 'pending'}
    return resp.content['registration']

def get_registration_jwt(user_id, expires_in=5 * 60):
    now = time.time()
    payload = {
        'iss': current_app.config['AUTHY_APP_NAME'],
        'iat': now,
        'exp': now + expires_in,
        'context': {
            'custom_user_id': str(user_id),
            'authy_app_id': current_app.config['AUTHY_APP_ID'],
        },
    }
    return jwt.encode(payload, current_app.config['AUTHY_PRODUCTION_API_KEY'])

def get_qrcode(jwt):
    qr = qrcode.make("authy://account?token=" + jwt,
                        image_factory=qrcode.image.svg.SvgImage)
    stream = BytesIO()
    qr.save(stream)
    return stream.getvalue()

def delete_authy_user(authy_id):
    authy_api = AuthyApiClient(current_app.config["AUTHY_PRODUCTION_API_KEY"])
    deleted = authy_api.users.delete(authy_id)
    return deleted.ok()


def verify_authy_token(authy_id, token):
    authy_api = AuthyApiClient(current_app.config["AUTHY_PRODUCTION_API_KEY"])
    verification = authy_api.tokens.verify(
        authy_id,
        token=token
    )
    return verification
