# Django Import
from cgitb import lookup
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.forms.models import model_to_dict
from rest_framework import status
# Rest Framework Import
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import RetrieveAPIView, ListAPIView,ListCreateAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser,AllowAny
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from posts.serializers import *
from django.http import JsonResponse



# Local Import
from posts.models import *






# # Get all the Posts with query
@api_view(['GET'])
def getPosts(request):  
    query = request.query_params.get("keyword")
    if query == None:
        query = ''
    lookup = Q( content__icontains=query)  
    posts = Post.objects.filter(lookup).order_by('-_id')
    posts_count = Post.objects.all().count()
    page = request.query_params.get('page')
    paginator = Paginator(posts, 20)

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    if page == None:
        page = 1
    page = int(page)

    serializer = PostsSerializer(posts, many=True)
    return Response({'posts': serializer.data,'count':posts_count ,'page': page, 'pages': paginator.num_pages})







# Get single post
@api_view(['GET'])
def getPost(request, pk):
    post = Post.objects.get(_id=pk)
    serializer = PostsSerializer(post, many=False)
    return Response({"post":serializer.data})



# Get My Posts
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getMyPosts(request,pk):
    query = request.query_params.get("keyword")
    user = User.objects.get(id=pk)
    if query == None:
        query = ''
    lookup = Q( content__icontains=query)  
    posts = Post.objects.filter(user=user).filter(lookup).order_by('-_id')
    posts_count = Post.objects.filter(user=user).count()
    page = request.query_params.get('page')
    paginator = Paginator(posts, 20)

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    if page == None:
        page = 1
    page = int(page)

    serializer = PostsSerializer(posts, many=True)
    return Response({'posts': serializer.data,'count':posts_count ,'page': page, 'pages': paginator.num_pages})
        
    
        
    
    
@api_view(['GET'])
def getComments(request, pk):
    post = Post.objects.get(_id=pk)
    comments = Comment.objects.filter(post=post).order_by("-_id")
    comment_count = Comment.objects.filter(post=post).count()
    
    serializer = CommentSerializer(comments, many=True)
    return Response({"comments": serializer.data, "count":comment_count})
    

        
   




# Create a new Post
@api_view(['POST'])
def createComment(request,pk):
    data = request.data
    post = Post.objects.get(_id=pk)

    if(data["content"] ==""):
        return Response({"Comment is Empty"})
    else:
        comment = Comment.objects.create(
            post=post,
            content=data["content"],
            
        )

        serializer = CommentSerializer(comment, many=False)
        return Response(serializer.data)
        
    

@api_view(['GET'])
def getPolls(request, pk):
    post = Post.objects.get(_id=pk)
    choices = Choice.objects.filter(post=post).all().order_by("-_id")
    choice_count = Choice.objects.filter(post=post).count()
    serializer = ChoiceSerializer(choices, many=True)
    return Response({"polls": serializer.data, "count":choice_count})




@api_view(['PUT'])
def addVote(request, pk):
    poll = Choice.objects.get(_id=pk)
    poll.votes+=1
    poll.save()
    serializer = ChoiceSerializer(poll, many=False)
    return Response({"poll":serializer.data})



# Create a new Post
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createPost(request):
    user = request.user
    post = Post.objects.create(
        user=user,
        title="Post Title",
        link=" link",
        content="Post Description",
        
    )

    serializer = PostsSerializer(post, many=False)
    return Response(serializer.data)



# Create a new Post
# @api_view(['POST'])
# @permission_classes([IsAuthenticated, IsAdminUser])
# def createNewPost(request):
    
#     data = request.data
#     print(data)
#     user_id = data['user']
#     user = User.objects.get(pk=user_id)
#     post = Post.objects.create(
#         user=user,
#         title=data['title'],
#         link=data['link'],
#         is_poll=data['is_poll'],
#         content=data['content'],
        
#     )

#     serializer = PostsSerializer(post, many=False)
#     print(serializer.data)
#     return Response({"post":serializer.data})


# Create a new Post
# Create a new Post
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createNewPost(request):
    
    data = request.data
    user_id = data['user']
    user = User.objects.get(pk=user_id)
    post = Post.objects.create(
        user=user,
        title=data['title'],
        link=data['link'],
        is_poll=data['is_poll'],
        content=data['content'],
        
    )
    if data['is_poll']:
        choice_texts = data['choices']
        choices = []
        for choice_text in choice_texts:
            choice = Choice.objects.create(
                post=post,
                choice_text=choice_text,
            )
            choices.append(choice)
        serializer = ChoiceSerializer(choices, many=True)
        return Response({"post": serializer.data, "choices": serializer.data})
    else:
        serializer = PostsSerializer(post, many=False)
        return Response({"post": serializer.data})



# Create a new Post
@api_view(['PUT'])
@permission_classes([IsAdminUser, IsAuthenticated])
def updatePost(request,pk):
    data =  request.data
    post = Post.objects.get(_id=pk)
    post.title = data["title"]
    post.content = data["content"]
    post.link = data["link"]
    post.is_poll = data["is_poll"]


    post.save()

    serializer = PostsSerializer(post, many=False)
    return Response({ "post":serializer.data})


# @api_view(['PUT'])
# @permission_classes([IsAdminUser, IsAuthenticated])
# def updatePost(request,pk):
#     data = request.data
#     post = Post.objects.get(_id=pk)
#     post.title = data.get("title", post.title)
#     post.content = data.get("content", post.content)
#     post.link = data.get("link", post.link)
#     post.is_poll = data.get("is_poll", post.is_poll)

#     if post.is_poll:
#         # If the post is a poll, update the choice objects
#         poll_choices = data.get("polls", [])
#         if poll_choices:
#             # Update existing choices or create new ones if they don't exist
#             for index, choice_text in enumerate(poll_choices):
#                 choice_id = data.get(f"choice_{index}_id")
#                 if choice_id:
#                     # If the choice ID is present in the data, update the existing choice
#                     choice = Choice.objects.get(id=choice_id, post=post)
#                     choice.choice_text = choice_text
#                     choice.save()
#                 else:
#                     # Otherwise, create a new choice
#                     choice = Choice(choice_text=choice_text, post=post)
#                     choice.save()

#     post.save()

#     serializer = PostsSerializer(post, many=False)
#     return Response({ "post":serializer.data})










# Create a new Post
@api_view(['POST'])
@permission_classes([IsAdminUser, IsAuthenticated])
def createNewPoll(request,pk):
    data =  request.data
    post = Post.objects.get(_id=pk)
    poll = Choice.objects.create(
        post=post,
        choice_text = data['choice_text']
        
    )

    poll.save()

    serializer = ChoiceSerializer(poll, many=False)
    return Response({ "poll":serializer.data})



# Create a new Post
@api_view(['POST'])
@permission_classes([IsAdminUser, IsAuthenticated])
def createPoll(request,pk):
    data =  request.data
    post = Post.objects.get(_id=pk)
    poll = Choice.objects.create(
        post=post,
        choice_text = "Choice Name"
        
    )

    poll.save()

    serializer = ChoiceSerializer(poll, many=False)
    return Response({ "poll":serializer.data})









@api_view(['PUT'])
@permission_classes([IsAdminUser, IsAuthenticated])
def updatePoll(request, pk):
    data = request.data
    poll = Choice.objects.get(_id=pk)
    poll.choice_text = data["choice_text"]
    poll.save()

    serializer = ChoiceSerializer(poll, many=False)
    return Response({"poll":serializer.data})



# Delete a post
@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deletePost(request, pk):
    post = Post.objects.get(_id=pk)
    post.delete()
    return Response("Post deleted successfully")


# Delete a post
@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deletePoll(request, pk):
    poll = Choice.objects.get(_id=pk)
    poll.delete()
    return Response("Poll deleted successfully")
