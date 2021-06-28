from flask import current_app
from datetime import datetime
from nesplash.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import BadSignature, SignatureExpired

# 帳號 username
# 名字 name
# 信箱 email
# 密碼 password
# 介紹 bio
# 地點 location
# 大頭照 profile_image
# 按讚 total_likes
# 收藏 total_collections
# 照片總數 total_photos
# unsplash連結 links -> html
# 驗證 confirmed
# 封禁 locked

# Role table
# 1.Locked 2.User 3.Administrator

# Permission table
# 1.FOLLOW 2.COLLECT 3.UPLOAD 4.ADMINISTER

class Method(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    users = db.relationship("User", back_populates="methods", cascade="all")

    @staticmethod
    def init_method():
        method_list = ["normal", "google", "github"]

        for method_name in method_list:
            method = Method(name=method_name)
            db.session.add(method)
        db.session.commit()


class Follow(db.Model):
    follower_id = db.Column(
        db.Integer, db.ForeignKey("user.id"), nullable=False, primary_key=True)
    followed_id = db.Column(
        db.Integer, db.ForeignKey("user.id"), nullable=False, primary_key=True)
    timestamp = db.Column(db.TIMESTAMP, nullable=True, default=datetime.utcnow)

    follower = db.relationship("User", foreign_keys=[follower_id], back_populates="following", lazy='joined')
    followed = db.relationship("User", foreign_keys=[followed_id], back_populates="followers", lazy="joined")

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.Text)
    bio = db.Column(db.Text, nullable=True)
    location = db.Column(db.String(50), nullable=True)
    profile_image = db.Column(db.String(255), nullable=False, default='https://dkn8b9qqzonkk.cloudfront.net/profile_pics/default.jpg')
    total_collections = db.Column(db.Integer, default=0)
    total_photos = db.Column(db.Integer, default=0)
    link = db.Column(db.String(255))
    lock_status = db.Column(db.Boolean, default=False)
    confirmed = db.Column(db.Boolean, default=False)

    role_id = db.Column(db.Integer, db.ForeignKey("role.id"))
    method_id = db.Column(db.Integer, db.ForeignKey("method.id"))

    role = db.relationship('Role', back_populates="users")
    photos = db.relationship('Photo', back_populates='author', lazy="joined", cascade="all")
    collections = db.relationship("Collection", back_populates="collector", cascade="all")
    methods = db.relationship("Method", back_populates="users")

    following = db.relationship("Follow", foreign_keys=[Follow.follower_id], back_populates="follower", lazy="dynamic", cascade="all")
    followers = db.relationship("Follow", foreign_keys=[Follow.followed_id], back_populates="followed", lazy="dynamic", cascade="all")

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        self.follow(self)
        self.set_role()

    def set_role(self):
        if self.role is None:
            if self.email == current_app.config["ADMIN_EMAIL"]:
                self.role = Role.query.filter_by(name="Administrator").first()
            else:
                self.role = Role.query.filter_by(name="User").first()
            db.session.commit()

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password, password)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config["SECRET_KEY"], expires_sec)
        return s.dumps({"user_id": self.id})
        
    @staticmethod
    def validate_token(token):
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            user_id = s.loads(token)["user_id"]
        except (BadSignature, SignatureExpired):
            return None
        return User.query.get(user_id)

    def upload_public_photo(self, user, description, category, clean_fn):
        if user is not None:
            photo = Photo(
                imageUrl=("https://dkn8b9qqzonkk.cloudfront.net/public_pics/" + clean_fn),
                description=description,
                download=("https://dkn8b9qqzonkk.cloudfront.net/public_pics/" + clean_fn),
                author=user,
                categorys=Category.query.filter_by(name=category).first()
            )
            self.total_photos += 1
            db.session.add(photo)
            db.session.commit()

    def follow(self, user):
        if not self.is_following(user):
            follow = Follow(follower=self, followed=user)
            db.session.add(follow)
            db.session.commit()

    def unfollow(self, user):
        follow = self.following.filter_by(followed_id=user.id).first()
        if follow:
            db.session.delete(follow)
            db.session.commit()

    def is_following(self, user):
        if user.id is None:  # when follow self, user.id will be None
            return False
        return self.following.filter_by(followed_id=user.id).first() is not None

    def locked(self):
        self.lock_status = True
        self.role = Role.query.filter_by(name="Locked").first()
        db.session.commit()

    def unlocked(self):
        self.lock_status = False
        self.role = Role.query.filter_by(name="User").first()
        db.session.commit()

    def collect(self, photo):
        if not self.is_collecting(photo):
            collect = Collection(collector=self, collected=photo)
            self.total_collections += 1
            db.session.add(collect)
            db.session.commit()

    def uncollect(self, photo):
        collect = Collection.query.with_parent(self).filter_by(collected_id=photo.id).first()
        if collect:
            self.total_collections -= 1
            db.session.delete(collect)
            db.session.commit()

    def is_collecting(self, photo):
        return Collection.query.with_parent(self).filter_by(collected_id=photo.id).first() is not None

    def can(self, permission_name):
        permission = Permission.query.filter_by(name=permission_name).first()
        if permission in self.role.permissions and permission is not None and self.role is not None:
            return True
        return False


class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    imageUrl = db.Column(db.String(255), nullable=True)
    description = db.Column(db.Text, nullable=True)
    download = db.Column(db.String(255), nullable=True)
    timestamp = db.Column(db.TIMESTAMP, nullable=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)

    author = db.relationship("User", back_populates="photos")
    categorys = db.relationship("Category", back_populates="photos")
    collectors = db.relationship("Collection", back_populates="collected", cascade="all")


class Collection(db.Model):
    collector_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, primary_key=True)
    collected_id = db.Column(db.Integer, db.ForeignKey("photo.id"), nullable=False, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    collector = db.relationship("User", back_populates="collections", lazy="joined")
    collected = db.relationship("Photo", back_populates="collectors", lazy="joined")


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    photos = db.relationship("Photo", back_populates="categorys", cascade="all")
    videos = db.relationship("Video", back_populates="categoryVideos", cascade="all")

    @staticmethod
    def init_category():
        category_list = ["architecture", "athletics", "food_drink", "nature", "people", "travel"]
        
        for category_name in category_list:
            category = Category(name=category_name)
            db.session.add(category)
        db.session.commit()


class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    videoUrl = db.Column(db.String(255))
    link = db.Column(db.String(255))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    categoryVideos = db.relationship("Category", back_populates="videos")

roles_permissions = db.Table("roles_permissions", 
                    db.Column("role_id", db.Integer, db.ForeignKey("role.id")),
                    db.Column("permission_id", db.Integer, db.ForeignKey("permission.id"))
                    )

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    users = db.relationship("User", back_populates="role")
    permissions = db.relationship("Permission", secondary=roles_permissions, back_populates="roles")

    @staticmethod
    def init_role():
        roles_permissions_map = {
            "Locked": ["FOLLOW", "COLLECT"],
            "User": ["FOLLOW", "COLLECT", "UPLOAD"],
            "Administrator": ["FOLLOW", "COLLECT", "UPLOAD", "ADMINISTER"]
        }

        for role_name in roles_permissions_map:
            role = Role.query.filter_by(name=role_name).first()
            if role is None:
                role = Role(name=role_name)
                db.session.add(role)
            role.permissions = []
            for permission_name in roles_permissions_map[role_name]:
                permission = Permission.query.filter_by(name=permission_name).first()
                if permission is None:
                    permission = Permission(name=permission_name)
                    db.session.add(permission)
                role.permissions.append(permission)
        db.session.commit()

class Permission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)
    roles = db.relationship("Role", secondary=roles_permissions, back_populates="permissions")
