import os
from flask import Flask, render_template, request, Response
from dotenv import load_dotenv
from app.Data_Loader import Data_Loader
import datetime
from peewee import *
from playhouse.shortcuts import model_to_dict
import re

load_dotenv()
app = Flask(__name__)

if os.getenv('TESTING') == 'true':
    print("Running on test mode")
    mydb = SqliteDatabase('file:memory?mode=memory&cache=shared', uri=True)
else: 
    mydb = MySQLDatabase(
        os.getenv("MYSQL_DATABASE"), 
        user = os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        host = os.getenv("MYSQL_HOST"),
        port = 3306
    )

class TimeLinePost(Model):
    name = CharField() 
    email = CharField()
    content = CharField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = mydb

mydb.connect()
mydb.create_tables([TimeLinePost])

DATA = Data_Loader()

def check(email): 
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$' 
    if(re.search(regex,email)):   
        return True 
    else:   
        return False

@app.route('/')
def landing_page():
    DATA = Data_Loader()
    return render_template('home.html',  data= DATA.skills_data)
    

@app.route('/about-me')
def about_me():
    return render_template('_about-me.html', data= DATA.about_me_data, url=os.getenv('URL'))

@app.route('/education-and-work-expirience')
def projects():
    return render_template('_education-and-work-expirience.html', data = DATA.expiriences_data, url=os.getenv('URL'))

@app.route('/projects')
def education():
    return render_template('_projects.html', data = DATA.projects_data, url=os.getenv('URL'))

@app.route('/timeline')
def timeline():
    return render_template('_timeline.html', data= DATA.about_me_data, title='Timeline', url=os.getenv('URL'))

@app.route('/base')
def base():
    return render_template('_landingPage.html', data = DATA.landing_page_data, landing_page=True, url=os.getenv('URL'))

@app.route('/api/timeline_post', methods=['POST'])
def post_time_line_post():
    try:
        name = request.form['name']
    except:
        return "Invalid name", 400
    email = request.form['email']
    if not email or check(email) == False: 
        return "Invalid email", 400
    content = request.form['content']  
    if not content:
         return "Invalid content", 400
    timeline_post = TimeLinePost.create(name=name, email=email, content=content)
    return model_to_dict(timeline_post)

@app.route('/api/timeline_post', methods=['GET'])
def get_timeline_post():
    return {
        'timeline_posts':[
            model_to_dict(post) 
            for post in 
            TimeLinePost.select().order_by(TimeLinePost.created_at.desc())
        ],
    }

@app.route('/api/timeline_post', methods=['DELETE'])
def delete_timeline_post():
    name = request.form['name']
    try:
        post = TimeLinePost.get(TimeLinePost.name == name)
        post.delete_instance()
    except:
        return Response(
            "Post not found",
            status=400,
        )
    return {"mesagge" : "deleted", "post":model_to_dict(post)}