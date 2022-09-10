from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

migrate = Migrate()
migrate.init_app(app, db)

from models import User, Post

@app.route("/")
def hello():
    return render_template("login.html")

@app.route("/post_creation_portal")
def post_portal():
    return render_template("add_post.html",user_id=request.args.get('user_id'))

@app.route("/create_account")
def create_account():
    return render_template("create_account.html")

@app.route("/login", methods=['POST'])
def login_user():
    uni=request.form.get('uni')
    try:
        user=User.query.filter_by(uni=uni).first()
        if (user is None):
            return "User does not exist. Please create an account first!"
    except Exception as e:
	    return(str(e))
    try:
        user=User.query.filter_by(uni=uni).first()
        all_posts = Post.query.all()
        posts = {}
        for post in all_posts:
            if (post.creating_user_id != user.id and post.reserving_user_id is None):
                posts[post.id] = {'description': post.description, 'dietary_info': post.dietary_info, 'img_url': post.img_url, 'user': User.query.filter_by(id=post.creating_user_id).first().name}
        return render_template("posts.html", posts=posts, user_id = user.id, points= user.points)
    except Exception as e:
	    return(str(e))
    
@app.route("/see_own_posts")
def see_own_posts():
    user_id=request.args.get('user_id')
    try:
        all_posts = Post.query.all()
        posts = {}
        for post in all_posts:
            if (post.creating_user_id == int(user_id)):
                posts[post.id] = {'description': post.description, 'dietary_info': post.dietary_info, 'img_url': post.img_url, 'user': User.query.filter_by(id=post.creating_user_id).first().name}
        return render_template("posts.html", posts=posts, user_id=user_id)
    except Exception as e:
	    return(str(e))

@app.route("/see_reserved_posts")
def see_reserved_posts():
    user_id=request.args.get('user_id')
    try:
        all_posts = Post.query.all()
        posts = {}
        for post in all_posts:
            if (post.reserving_user_id == int(user_id)):
                posts[post.id] = {'description': post.description, 'dietary_info': post.dietary_info, 'img_url': post.img_url, 'user': User.query.filter_by(id=post.creating_user_id).first().name}
        return render_template("posts.html", posts=posts, user_id=user_id)
    except Exception as e:
	    return(str(e))

@app.route("/name/<name>")
def get_book_name(name):
    return "name : {}".format(name)

@app.route("/getall")
def get_all():
    try:
        posts=Post.query.all()
        return  jsonify([e.serialize() for e in posts])
    except Exception as e:
	    return(str(e))

@app.route("/get/<id_>")
def get_by_id(id_):
    try:
        user=User.query.filter_by(id=id_).first()
        return jsonify(user.serialize())
    except Exception as e:
	    return(str(e))

@app.route("/add_user",methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        name=request.form.get('name')
        uni=request.form.get('uni')
        try:
            user=User(
                name=name,
                uni=uni
            )
            db.session.add(user)
            db.session.commit()
            all_posts=Post.query.all()
            posts = {}
            for post in all_posts:
                posts[post.id] = {'description': post.description, 'dietary_info': post.dietary_info, 'img_url': post.img_url, 'user': User.query.filter_by(id=post.creating_user_id).first().name}
            return render_template("posts.html", posts=posts, user_id=user.id)
        except Exception as e:
            return(str(e))
    return render_template("getdata.html")

@app.route("/add_post",methods=['GET', 'POST'])
def add_post():
    if request.method == 'POST':
        description=request.form.get('description')
        dietary_info=request.form.get('dietary_info')
        img_url=request.form.get('img_url')
        user_id=request.form.get('user_id')
        user = User.query.filter_by(id=user_id).first()
        try:
            post=Post(
                description=description,
                dietary_info=dietary_info,
                img_url=img_url,
                author=int(user_id),
            )
            db.session.add(post)
            user.points += 1
            db.session.commit()
            all_posts=Post.query.all()
            posts = {}
            for post in all_posts:
                if (post.creating_user_id != int(user_id) and post.reserving_user_id is None):
                    posts[post.id] = {'description': post.description, 'dietary_info': post.dietary_info, 'img_url': post.img_url, 'user': User.query.filter_by(id=post.creating_user_id).first().name}
            return render_template("posts.html", posts=posts, user_id=user_id)
        except Exception as e:
            return(str(e))
    return render_template("getdata.html")

@app.route("/reserve",methods=['GET'])
def reserve_food():
    if request.method == 'GET':
        post_id=request.args.get('post_id')
        user_id=request.args.get('user_id')
        try:
            post = Post.query.filter_by(id=post_id).first()
            post.reserving_user_id = user_id
            user = User.query.filter_by(id=user_id).first()
            if (user.points == 0):
                return "You don't have enough points to reserve a meal!"
            user.points -= 1
            db.session.commit()
            return  "You have successfully reserved this meal!"
        except Exception as e:
            return(str(e))
    return render_template("getdata.html")

@app.route("/cancel_reservation",methods=['GET'])
def cancel_reservation():
    post_id=request.args.get('post_id')
    user_id=request.args.get('user_id')
    post = Post.query.filter_by(id=post_id).first()
    user = User.query.filter_by(id=user_id).first()
    post.reserving_user_id = None
    user.points += 1
    db.session.commit()
    return show_profile()

@app.route("/remove_offering",methods=['GET'])
def delete_offering():
    post_id=request.args.get('post_id')
    user_id=request.args.get('user_id')
    post = Post.query.filter_by(id=post_id).first()
    user = User.query.filter_by(id=user_id).first()
    db.session.delete(post)
    user.points -= 1
    db.session.commit()
    return show_profile()

@app.route("/profile",methods=['GET'])
def show_profile():
    user_id=request.args.get('user_id')
    user = User.query.filter_by(id=user_id).first()
    all_posts = Post.query.all()
    reserved_posts = {}
    created_posts = {}
    for post in all_posts:
        if (post.reserving_user_id == int(user_id)):
            reserved_posts[post.id] = {'description': post.description, 'dietary_info': post.dietary_info, 'img_url': post.img_url, 'user': User.query.filter_by(id=post.creating_user_id).first().name}
        if (post.creating_user_id == int(user_id)):
            created_posts[post.id] = {'description': post.description, 'dietary_info': post.dietary_info, 'img_url': post.img_url, 'user': User.query.filter_by(id=post.creating_user_id).first().name}
    return render_template("profile.html", points=user.points, user_id=user_id, reserved_posts=reserved_posts, created_posts=created_posts)


if __name__ == '__main__':
    app.run()