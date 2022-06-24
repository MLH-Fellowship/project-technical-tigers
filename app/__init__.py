import os
from flask import Flask, render_template, request, Response
from dotenv import load_dotenv
from app.Data_Loader import Data_Loader
import datetime
from peewee import *
from playhouse.shortcuts import model_to_dict

load_dotenv()
app = Flask(__name__)

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

@app.route('/')
def landing_page():
    return render_template('landingPage.html', data = DATA.landing_page_data, landing_page=True, url=os.getenv('URL'))

@app.route('/about-me')
def about_me():
    return render_template('about-me.html', data= DATA.about_me_data, url=os.getenv('URL'))

@app.route('/education-and-work-expirience')
def projects():
    return render_template('education-and-work-expirience.html', data = DATA.expiriences_data, url=os.getenv('URL'))

@app.route('/projects')
def education():
    return render_template('projects.html', data = DATA.projects_data, url=os.getenv('URL'))

@app.route('/api/timeline_post', methods=['POST'])
def post_time_line_post():
    name = request.form['name']
    email = request.form['email']
    content = request.form['content']   
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