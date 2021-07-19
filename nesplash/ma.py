from nesplash.extensions import ma

class PhotoSchama(ma.Schema):
    class Meta:
        fields = ('id', 'imageurl', 'description','download', 'timestamp', 'category_id', 'label')


class VideoSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "link", "videourl")


class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "username", "profile_image", "link", "bio", "location",
                "total_likes", "total_photos", "total_collections", "confirmed", "lock_status")

class CollectionSchema(ma.Schema):
    class Meta:
        fields = ("collector_id", "collected_id", "timestamp")

class FollowSchema(ma.Schema):
    class Meta:
        fields = ("follower_id", "followed_id", "timestamp")



photoSchema = PhotoSchama(many=True)
videoSchema = VideoSchema(many=True)
userSchema = UserSchema(many=True)
collectionSchema = CollectionSchema(many=True)
followSchema = FollowSchema(many=True)
