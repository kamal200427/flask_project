from flask import Flask,render_template,request,redirect,flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_login import LoginManager,login_user,UserMixin,logout_user
from  datetime import datetime 
class Base(DeclarativeBase):
  pass
db = SQLAlchemy(model_class=Base)
app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///main.db"
app.config["SECRET_KEY"]="thisissecret"
# initialize the app with the extension
db.init_app(app)

class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), unique=False, nullable=False)
    fname= db.Column(db.String(50), unique=False, nullable=False)
    lname= db.Column(db.String(50), unique=False, nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
# Route to create new user
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        fname = request.form["fname"]
        lname = request.form["lname"]
        name = request.form["username"]
        user = User(email=email,password=password,fname=fname,lname=lname,username=name)
        db.session.add(user)
        db.session.commit()
        print(user.password)
        flash('register successfully','success')
        return redirect("/login")
    return render_template("register.html")
    
login_manager = LoginManager()
login_manager.init_app(app)
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
  
@app.route("/login",methods=['GET', 'POST'])
def user_list():
    # users = User.query.all()
    if request.method=="POST":
        username = request.form["username"]
        password=request.form["password"]
        user=User.query.filter_by(username=username).first()
        if user and password==user.password:
            login_user(user)
            return redirect(f"/diagram/{user.username}")
        else:
            flash("invalid username","danger")
            return redirect("/login")
    return render_template("login.html")

#blog page code
class Blog(db.Model):
    blog_id = db.Column(db.Integer, primary_key=True)
    room= db.Column(db.Integer, nullable=False)
    dinning= db.Column(db.Integer, nullable=False)
    washroom = db.Column(db.Integer, nullable=False)
    pub_date = db.Column(db.DateTime(), nullable=False,default=datetime.now)
#     # repr method represents how one object of this datatable
#     # will look like
@app.route("/logout")
def logout():
    logout_user()
    return redirect("/main")
    

@app.route("/diagram/<string:username>",methods=['GET','POST'])
def diagram(username):
    bio=User.query.filter_by(username=username).first()
    if request.method == "POST":
        print("form submitted")
        room=request.form["room"]
        dinning=request.form["dinning"]
        washroom=request.form["washroom"]
        data=Blog(room=room,dinning=dinning,washroom=washroom)
        db.session.add(data)
        db.session.commit()
        # flash("Post is sent succcessfully","success")
        # value+=room*1000+dinning*500+washroom*
        return redirect(f"/bill_print/{bio.username}/{data.blog_id}")
    return render_template("diagram.html")
@app.route("/main")
def main():
    return render_template("main.html")
@app.route("/")
def index():
    # data=Blog.query.all()
    return render_template("main.html")


@app.route("/bill_print/<string:username>/<int:id>")
def blog_detail(username,id):
    bio=User.query.filter_by(username=username).first()
    blog=Blog.query.get_or_404(id)
    # value=0
    # for i in blog:
        # value+=i
    return render_template("bill.html",blog=blog,bio=bio)

# @app.route("/blog_delete/<int:id>")
# def delete_post(id):
#     data=Blog.query.get(id)
#     db.session.delete(data)
#     db.session.commit()
#     flash("The massage is deleted  sucessfully","success")
#     return redirect("/")

# @app.route("/blog_edit/<int:id>",methods=['GET','POST'])
# def edit_post(id):
#     blog=Blog.query.get(id)
#     if request.method=="POST":
#         blog.title=request.form.get("title")
#         blog.author=request.form.get("author")
#         blog.content=request.form.get("content")
#         db.session.commit()
#         flash("The massage is updated sucessfully","success")
#         return redirect("/")
#     return render_template("edit.html",blog=blog)


if __name__=="__main__":
    # print(" kamal")
    app.run(debug=True)
    