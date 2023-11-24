from rest_framework import serializers

from apps.post.models import Post


class PostCreateUpdateDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["text", "media_url"]

    def create(self, validated_data):
        user = self.context["request"].user
        Post.objects.create(
            text=validated_data.get("text"),
            media_url=validated_data.get("media_url"),
            user=user
        )
        return validated_data

    def update(self, instance, validated_data):
        instance.text = validated_data.get("text", instance.text)
        instance.media_url = validated_data.get("media_url", instance.media_url)
        instance.save()
        return instance


class PostListRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"


class PostLikeDislikeSerializer(serializers.Serializer):
    post_id = serializers.IntegerField()

    def validate_post_id(self, post_id):
        try:
            post = Post.objects.get(id=post_id)
            return post_id
        except Post.DoesNotExist:
            raise serializers.ValidationError("Post dose not exist!")
