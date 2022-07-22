import os
from flask import Flask, render_template, request, Response
from dotenv import load_dotenv
from app.Data_Loader import Data_Loader
from app.utils import check_email
import datetime
from peewee import *
from playhouse.shortcuts import model_to_dict

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

@app.route('/')
def landing_page():
    DATA = Data_Loader()
    return render_template('home.html',  skills_data= DATA.skills_data, experiences_data = DATA.experiences_data)
    
@app.route('/timeline')
def timeline():
    DATA = Data_Loader()
    return render_template('_timeline.html', data= DATA.about_me_data, title='Timeline', url=os.getenv('URL'))

@app.route('/api/timeline_post', methods=['POST'])
def post_time_line_post():
    try:
        name = request.form['name']
    except:
        return "Invalid name", 400
    email = request.form['email']
    if not email or check_email(email) == False: 
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