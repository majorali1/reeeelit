from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages # used for sending messages type in htmll using template tags aswell
from django.http import HttpResponse


from .model import User,Post,Comment,Like_dislike

# Create your views here.




# second task : exception checks and refine a bit of all
# static on htmls and design them
# difine logout and thats it




# thats it for now




def main(request):
    cookie = request.COOKIES.get('email')
    response = render(request,"mainpage.html")
    if cookie:
        response = render(request,"mainpage.html",{"email":cookie})
    
    posts = Post.objects.values().order_by('-created_at')[:7]
    response = render(request,"mainpage.html",{"email":cookie,"posts":posts})
    return response
    




def postsignup(request):
    if request.method == 'GET':
        return render(request,"signup.html")
    

    name = request.POST.get('name')
    email = request.POST.get('email')
    password : int = request.POST.get('password')

    if not name and email and password:
        return redirect('postsignup')
    user = User.objects.filter(name=name,email=email,password=password)
    if user:
        messages.info(request,"login pls already signin")
        return redirect('getlogin')

    user = User(name=name,email=email,password=password)
    user.save()
    return redirect('getlogin')
    

def getlogin(request):    
    return render(request,'login.html')

def postlogin(request):
    email = request.POST.get('email')
    password : int = request.POST.get('password')

    if not email and password:
        return redirect('getlogin')

    user = User.objects.filter(email=email,password=password)

    if user:
        response = render(request,"successful.html")
        response.set_cookie(key='email',value=email,max_age=600 * 600)
        
        return response

    failed = "signup failed please try again"
    return render(request,"signup.html",{"failed":failed})


"""

this func was to test context and send data from backend to html 

def test(request):
    email = request.COOKIES.get('email')
    if email:
        return render(request,"mainpage.html",{"email":email})
    
    return HttpResponse('nope')

"""

def logout(request):
    email = request.COOKIES.get('email')
    if not email:
        return redirect('signup')
    logout = "Sucessfully logged out!"
    response = render(request,"successful.html",{"logout":logout})
    response.delete_cookie('email')
    return response








#after login send user to dashboard and a create post button



def dashboard(request):

    email = request.COOKIES.get('email')

    if not email:
        return redirect('getlogin')
    
    user = User.objects.filter(email=email).first()

    if not user:
        return redirect('signup')
    response = render(request,"dashboard.html",{"email":user.email,"name":user.name})
    return response        


def getpostcreation(request):
    return render(request,"postcreater.html")


#this will be changed later idk what to do rn
#the change i am thinking is where will user go after post is created to the post itself?
#or someplace else?
def publishpost(request):
    
    email = request.COOKIES.get('email')
    
    if not email:
        return redirect('signup')
    

    title = request.POST.get('title')
    content = request.POST.get('content')
    if not title and content:
        return HttpResponse(404)
        
    user = User.objects.get(email=email)
    response = redirect('dashboard')
    

    post = Post(title=title,content=content,created_by=user)
    post.save()
    return response


# this is mini posts cards first version
"""
def miniposts(request):
    post = Post.objects.all().values()
    return render(request,"thepost.html",{"post":post})
"""

#this view represensts alot of what i needed but i did it myself so yaay
def fullpost(request,id):


    mainpost = Post.objects.filter(id=id).first()

    if not mainpost:
        return HttpResponse(404)
    
    comments = Comment.objects.filter(post=mainpost)
    likes = Like_dislike.objects.filter(like=True).count()
    dislikes = Like_dislike.objects.filter(dislike=True).count()

    if request.method == "POST":
        email = request.COOKIES.get('email')
        if email:
            user = User.objects.get(email=email)
            comment = request.POST.get('comment')

            savecomment = Comment(user=user,content=comment,post=mainpost)
            savecomment.save()
         
            return redirect('fullpost',id=id)
        else:
            return redirect('signup')
    
    
    
    
    return render(request,"mainpost.html",{"fullpost":mainpost,"likes":likes,"dislikes":dislikes,"comments":comments})

# find a way so that in same page u can send a comment and can view comment
#wth are u saying i dont get it


def test(request):
    return HttpResponse("oo")


def likepost(request,id):
    use = request.COOKIES.get('email')
    if use:
        
        user = User.objects.get(email=use)
    else:
        return redirect('signup')
    post = Post.objects.get(id=id)

    likes,created = Like_dislike.objects.get_or_create(user=user,post=post)

    if created:
        likes.like = True
        likes.dislike = False
    else:
        if likes.like:
            likes.like = False
        else:
            likes.like=True
            likes.dislike=False
    likes.save()

    return redirect('fullpost', id=post.id)

def dislikepost(request,id):
    email = request.COOKIES.get('email')

    if not email:
        return redirect("getlogin")
    
    user = User.objects.filter(email=email).first()

    if not user:
        return redirect('getlogin')

    try:
        post = Post.objects.get(id=id)
    except Post.DoesNotExist:
        return redirect('main')    

    dislikes,created = Like_dislike.objects.get_or_create(user=user,post=post)
    if created:
        dislikes.dislike = True
        dislikes.like = False
    else:
        if dislikes.dislike:
            dislikes.dislike= False
        else:

            dislikes.dislike = True
            dislikes.like = False
    dislikes.save()
    return redirect("fullpost", id=post.id)



#   dislikes,created = Like_dislike.objects.get_or_create(user=user,post=post)
# remember this it uses 2 variables and u can use it to check if a database row is created or not so u can update it if created else make a new row 

#check html postcreater to find help related to getting multiple posts of single user 
# so later on we can get multiple posts send to html remember to check html ok





"""
def likepost(request):
    #in this func first check for user if loggedin then ceck the post like he clicked then save it and send like updated count
    email = request.COOKIES.get('email')
    if email:
        user = User.objects.filter(email=email).first()
        post =Post.objects.get(id=1)
        
        return redirect("fullpost",id=1)
    return redirect('postsignup')

def dislikepost(request):    
    #in this func first check for user if loggedin then ceck the post like he clicked then save it and send like updated count
    email = request.COOKIES.get('email')
    if email:
        user = User.objects.filter(email=email).first()
        post =Post.objects.get(id=1)
        
        return redirect("fullpost",id=1)
    return redirect('postsignup')

"""


def deletepost(request):
    return HttpResponse()

def updatepost(request):
    return HttpResponse()