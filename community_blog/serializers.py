from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from community_blog.models import *

class PostSerializer(serializers.HyperlinkedModelSerializer):
    #author = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='author', write_only=True)
    #author = serializers.ReadOnlyField(source='author.username')
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), default=serializers.CurrentUserDefault())

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'post_created_timestamp', 'post_updated_timestamp', 'author']

class CommentSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = Comment
        fields = ['id', 'post_id', 'comment_content', 'comment_created_timestamp', 'comment_updated_timestamp', 'author']

class UserSerializer(serializers.ModelSerializer):
    #posts = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
	posts = PostSerializer(many=True)

    class Meta:
        model = User
        fields = ['id','username', 'email', 'password', 'posts']

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'username']

    def create(self, validated_data):
        password_hash=User.objects.create_user(username=validated_data['username'], email=validated_data['email'])
        password_hash.set_password(validated_data['password'])
        password_hash.save()
        return password_hash