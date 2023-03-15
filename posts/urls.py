from django.urls import path
from posts.views import *


urlpatterns = [


    

    # create new post
    path('create/', createNewPost,name="create-new-post"),
    path('<str:pk>/comment/create/', createComment, name="create-comment"),
      # create poll
    path('polls/<str:pk>/create/', createPoll, name="create-New-poll"),

     # create post
    path('add/', createPost,name="create-post"),

     # get post
    path('<str:pk>/', getPost,name="get-post"),


   
    # get posts
    path('', getPosts,name="Posts"),

    # get my post
    path('<str:pk>/myposts/', getMyPosts,name="My Posts"),
    # get post
    path('<str:pk>/', getPost,name="get-post"),

    # update post
    path('update/<str:pk>/', updatePost,name="get-post"),

   

    


    # create comment
    path('<str:pk>/comment/create/', createComment, name="create-comment"),


    # get comments
    path('comments/<str:pk>/', getComments, name="get-comments"),


    # get polls
    path('polls/<str:pk>/', getPolls, name="get-polls"),

   

    # create poll
    path('polls/<str:pk>/delete/', deletePoll, name="delete-poll"),
    # create poll
    path('<str:pk>/delete/', deletePost, name="delete-post"),

    # update poll
    path('polls/<str:pk>/update/', updatePoll, name="update-poll"),

    # vote
    path('polls/<str:pk>/vote/', addVote, name="vote")
    
    
]
