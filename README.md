# django_project_practice
Django Application: A platform to save personal music, create playlists, mark favorites and search songs and albums available. It will also have a user login feature.


# DJANGO STEPS
open powershell as an admin

## check python version
```
python --version
```
## check pip version
```
pip --version
```
## upgrade pip if required
```
python -m pip install --upgrade pip
```
## install django
```
pip install django
```
or
```
easy_install django
```
## check django version
```
django-admin --version
```
## create a django project
```
django-admin startproject <name>
```
example -:
```
django-admin startproject website
```
## Create an app
```
python manage.py startapp app_name
```

## Run Server
```
python manage.py runserver
```
this server runs continously and will keep refreshing the server automatically when a change is detected

## Stop the Server
```ctrl+c```

## sync up the database with your source code
```
python manage.py migrate
```
## Whenever a new app is created, add it in settings.py under INSTALLED_APPS, to make sure the website knows of what all apps have been created
example:
### Before
```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
```
### After
```
INSTALLED_APPS = [
    'music.apps.MusicConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
```
## After adding the app, the server looks for each models provided for each apps, so to make sure it finds it.
```
python manage.py makemigrations music
```

## To check what you migrated
```
python manage.py sqlmigrate music 0001
```
now sync up the source code with the database again


## To access the interactive shell
```
python manage.py shell
```

### inside the shell connect to the database
```
from music.models import Album, Song
```

### view all object available in the database
```
Album.objects.all()
Song.objects.all()
```

### Insert into the database
```
a = Album(artist="Taylor Swift", album_title="Red", genre="Pop", album_logo="https://upload.wikimedia.org/wikipedia/en/c/c0/Taylor_Swift_-_Red_%28Single%29.png")
```
 or
```
b = Album()
b.artist = "One Direction"
b.album_title = "Native"
b.genre = "Pop"
b.album_logo = "https://upload.wikimedia.org/wikipedia/en/9/96/OneRepublic_-_Native.png"
```
### Save the content in the database - Without this step nothing will be written in the database
```
a.save()
b.save()
```
### View specific contents in the database

#### View by id
```
Album.objects.filter(id=1)
```
#### View by column name where data starts with
```
Album.objects.artist__startswith='Taylor'
```
#### View by column name where data ends with
```
Album.objects.artist__endswith='Taylor'
```

### how to insert into a database that uses a ForeignKey
```
from music.models import Song, Album
album1 = Album.objects.get(pk=1)
song = Song()
#set the value of album1 in song.album
song.album = album1 
song.file_type = 'mp3'
song.song_title = "Dear John"
song.save()
```
or 

### Display all songs associated with the album
```
album1.song_set.all()
```
### Add new songs to the album object with the help of create functions which automatically saves it in the database.
album1.song_set.create(song_title="Shake it off", file_type="mp3")
<Song: Shake it off>

### Count number of objects in that class
```
album1.song_set.count()
```


# Admin

## To create a admin user
```
python manage.py createsuperuser
```
Django comes with this default feature for an admin handler, after excecuting the above command we are prompted to provide details like username, email, password.
This will give them access as an admin to create, delete, modify.

## Add your models in the admin page
```
from .models import Album
```
### Register your Album class in the admin site
```
admin.site.register(Album)
```
refresh the server


## in the models page the __str__ functions will be shown in your admin page to access that record in the database
```
def __str__(self):
	return self.album_title + ' - ' + self.artist
```

# Views

Views has all the response to the request the user sends.
This is basically the page where we can find the differnt pages that will be available for your app.


```
from django.http import HttpResponse
```
this command is used to enable your view to return Http Response based on the request 

## in views
```
def detail(request, album_id):
    try:
        album = Album.objects.get(pk=album_id)
    except AlbumDoesNotExist:
        raise Http404("Album Does not exist")
    return render(request, 'music/detail.html', {'album': album})
```

the album_id argument comes from the url.py where we have defined our regular expression

```
re_path(r'^(?P<album_id>[0-9]+)/$', views.detail, name='detail')
```

the view will treat it as a variable and will send us response based on that value



# Templates

create this folder in your apps root directory name it as templates.
By default Django will automatically point to this folder for templates.
Create a sub folder inside that and name it the same as your app.

## python codes go under {% logic %}
## python variables go under {{ variable_name }}

```
{% if all_albums %}
    <ul>
        {% for album in all_albums %}
        <li><a href="/music/{{ album.id }}/">{{ album.album_title }}</a></li>
        {% endfor %}
    </ul>
{% else %}
    <h3>You dont have any albums to display</h3>
{% endif %}
```

```
from django.shortcuts import render
```

This allows you to render your template
it takes your http request, template, and the information that your template needs to perform
render will convert it to an actual http response


## raising an HTTP 404 Error

```
def detail(request, album_id):
    try:
        album = Album.objects.get(pk=album_id)
    except Album.DoesNotExist:
        raise Http404("Album Does not exist")
    return render(request, 'music/detail.html', {'album': album})
```

the code will check if album_id is matching any primary key in the database
and return us a result if it exists else it will Display the 404 error


## Removing Hardcodede URLs
to have dynamic urls, we need to use the name attribute defined for each url in our url.py script

{% url '<name>' <if any other pattern is associated> %}

### Before
```
<li><a href="/music/{{ album.id }}/">{{ album.album_title }}</a></li>
```


### After

```
<li><a href="{% url 'detail' album.id %}/">{{ album.album_title }}</a></li>
```


## Namespace

What if there is a scenario where another app uses the same name for their url?
How will django distinguish between them?

So to counter that they can do this :

in the url.py script add your app name
```
app_name = 'music'
```

and then in your template add <app name>:<name used for url>
```
<li><a href="{% url 'music:detail' album.id %}">{{ album.album_title }}</a></li>
```

## HTTP 404 shortcut

Django comes with a shortcut so that we dont have to write a logic for the 404 error
The get_object_or_404 will take your arguments and then if it fails to match, then it will throw its default 404 error page
```
from django.shortcuts import get_object_or_404 

def detail(request, album_id):
    album = get_object_or_404(Album, pk=album_id)
    return render(request, 'music/detail.html', {'album': album})

```


## Use of Static files
create a folder named static, Django will point here for static objects like css, images, javascript files
```
{% load staticfiles %}
```

use this command to load the files present in the static folder



## Bootstrap Links

### CSS
```
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.0/css/bootstrap.min.css">
```
### Ajax
```
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
```
### Javascript
```
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.0/js/bootstrap.min.js"></script>
```

## Using Base Templates

We use a base template which will contain all the similar styles used throughout the website.
This will help use reuse the same code but in a more efficient way

```
{% extends 'music/base.html' %}
```
including this in your webpage will allow you to access your base template design.


```
{% block <name> %}
---Statements---
---Statements---
---Statements---
{% endblock %}
```

we use this to include the code within the template body



# Using Generic Views

Django came up with a way to simplify our job of creating views that either show us a list view
or that show us a detailed view.

We use 'class' to define a generic view


```
class IndexView(generic.ListView):
    template_name = 'music/index.html'

    def get_queryset(self):
        return Album.objects.all()
```

```
template_name = '<path>/<name>.html'
```

This holds what template page we will display our result in.

Now in url.py, we are used to sending it function names for pointing a certain url to it.
But right now we are using class, so to define a url, What we can do is

```
path('', views.<class_name>.as_view(), name='index'),
```



### Whenever we are using a DetailView it expects a primary key in order to access the result.
```
re_path(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
```

### We define the model name for a DetailView
```
class DetailView(generic.DetailView):
    model = Album
    template_name = 'music/detail.html'
```


### Whenever we use a ListView it queries an object list
so the result is returned in a Default variable 

```
{% for album in object_list %}
```

to overwrite it we can use a variable 'context_object_name' and assign it a name that we want to use

```
context_object_name = 'all_albums'
```
after that use the same variable in your webpage to access that object
```
{% for album in all_albums %}
```


# Django Model Forms

Model Forms are used for speeding up the building process,
they generate the HTML code for us with basic form and they also perform form validations,
example if there are mandatory fields then it will prompt us with a reply like this cant be blank.
They take care of saving the data into the database

```
import django.url import reverse
```

add this function in the Album calss in models.py

```
    def get_absolute_url(self):
        return reverse('music:detail', kwargs={'pk': self.pk})
```


in Views create new classes

CreateView, UpdateView and DeleteView

```
from django.views.generic.edit import CreateView, UpdateView, DeleteView
```


```
class AlbumCreate(CreateView):
    model = Album
    fields = ['artist','album_title','genre','album_logo']
```

We need to provide information like what kind of object are we going to create

```
model = Album
```

What fields do we need, what attributes do we want the user to fill out

```
fields = ['artist','album_title','genre','album_logo']
```

after that create a url pattern in url.py
```
    # music/album/add
    re_path(r'album/add/$', views.AlbumCreate.as_view(), name='add_album'),
```


## to create a template for the form 

we need to go to the template directory and then inside the app directory where we will create the file with the name as 

<model_name/class_name>_<form>

all in lower case

example

album_form.html


## UpdateView

This will contain the name of the fields that you want to update and the name of the model that you will be working on
```
class AlbumUpdate(UpdateView):
    model = Album
    fields = ['artist','album_title','genre','album_logo']
```

## DeleteView

This will contain the name of the model you want to delete from and the page you want to redirect to once you have deleted your object

```
class AlbumDelete(DeleteView):
    model = Album
    success_url = reverse_lazy('music:index')
```


# Adding media to your Website

create a directory media in your project directory

go to the settings.py and towards the end set the path of your media directory

```
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

MEDIA_URL = '/media/'
```


now go to your URL.py in your project directory

```
from django.conf import settings
from django.conf.urls.static import static
```

these two are used to import the settings.py for your project and static function
add this towards the end

```
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```


the settings.DEBUG holds the value as true during development and when the product is sent for live,
we need to set the value to false

we are adding these media urls in our ```urlpatterns``` using the static function
which will take 
```
static(<variable_defined>, document_root=<variable_root>)
```

this will hold the value that was defined in settings.py 



# Creating user models and Creating Accounts

we will inherit this class from django.views.generic 

```
from django.views.generic import View
```

first thing we need to specify is what will be the blueprint for out form
```
form_class = UserForm
```

then we need to specify the template name we will be using for our form

```
template_name = 'music/registration_form.html'
```



