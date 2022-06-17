from django.shortcuts import render
#from django.http import JsonResponse

from rest_framework import viewsets
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework import status

from community_blog.models import *
from community_blog.serializers import *

from rest_framework.views import APIView
#from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework import generics



##Get curently signed user
@api_view(['GET'])
#@authentication_classes([SessionAuthentication, BasicAuthentication])
#@permission_classes([IsAuthenticated])
def current_user(request, format=None):
    #authentication_classes = [authentication.TokenAuthentication]
    #permission_classes = [permissions.IsAuthenticated]

    return Response({
        'user': str(request.user),
        'email': str(request.user.email),
        'id': str(request.user.id)
    })


@api_view(['GET', 'POST'])
def get_all_posts(request):

    #Display all posts
    if request.method == 'GET':
        posts = Post.objects.all()
        post_serializer = PostSerializer(posts, many=True)
        
		return Response({
			"message": "Success!",
			"data": {
				post_serializer.data
            }
        })
		
        return Response(post_serializer.data)


    #Create new post
    if request.method == 'POST':
        post_serializer = PostSerializer(data=request.data)

        if post_serializer.is_valid():
            post_serializer.save(author=request.user)
            return Response(post_serializer.data)
        return Response(post_serializer.errors)

#Get current user's posts
@api_view(['GET'])
def get_user_post(request):

    user = request.user
    posts = Post.objects.filter(author=user)
    post_serializer = PostSerializer(posts, many=True)
    
    return Response(post_serializer.data)


@api_view(['GET', 'PUT', 'DELETE'])
def get_post(request, id):

    try:
        post = Post.objects.get(pk=id)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        post_serializer = PostSerializer(post)
        return Response(post_serializer.data)

    #Update Post
    elif request.method == 'PUT':
        post_serializer = PostSerializer(post, data=request.data)

        if post_serializer.is_valid():
            post_serializer.save()
            return Response({
                "message": "Post updated!",
                'data': {
                    post_serializer.data
                }
            })
        return Response(post_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #Delete Post
    elif request.method == 'DELETE':
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


#Add Comment to a Post
# @api_view(['GET', 'POST'])
# def add_comment(request, id):

#     try:
#         comment = Comment.objects.get(pk=id)
#     except Post.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'GET':
#         comment_serializer = CommentSerializer(comment)
    
#     post_serializer = PostSerializer(data=request.data)

#     if post_serializer.is_valid():
#         post_serializer.save(author=request.user, post_id=id)

#         return Response({
#             "message": "Post created!",
#             'data': {
#                 post_serializer.data
#             }
#         })


#########################CLASS BASED VIEWS##############################3

class ListUsers(APIView):
    #authentication_classes = [authentication.TokenAuthentication]
    #permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        emails = [user.email for user in User.objects.all()]
        return Response(emails)

#Login
class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            "message": "Login successful!",
            "data": {
                'token': token.key,
            }
        })


# Register Api
class Register(APIView):

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({'message': 'Something went wrong'})

        serializer.save()
        user=User.objects.get(username=serializer.data['username'])
        token,created = Token.objects.get_or_create(user=user)

        return Response({
            "message": "Signup successful!",
            'data':{
                'user_id': user.pk,
                'email': user.email,
                'username': user.username,
            }
                
        })





