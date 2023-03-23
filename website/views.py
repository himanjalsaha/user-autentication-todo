from website import create_app
from flask import Blueprint,render_template,request,flash,redirect,url_for
from .models import User , Note
from werkzeug.security import generate_password_hash,check_password_hash
from . import db
from flask_login import login_user,login_required,logout_user, current_user


views=Blueprint('views',__name__)


@views.route("/",methods=['GET','POST'])
def login():
    if request.method=='POST':
        email=request.form.get('email')
        password=request.form.get('password')

        user=User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password,password):
                flash('logged in',category='successs')
                login_user(user,remember=True) 

                return redirect("/home")    
            else: 
                flash('incorrect password',category='error')    
        else:
            flash('email does not exist ',category='error')    
    return render_template("login.html")

@views.route("/signup",methods=['GET','POST'])
def signup():
    if request.method=='POST':
        name=request.form.get('name')
        email=request.form.get('email')
        password=request.form.get('password')
        password2=request.form.get('password2')

        user=User.query.filter_by(email=email).first()
        if user:
             flash('email Already exists ',category='error')
            

        if len(email) < 5:
            flash("Email is too short",category="error")
        elif len(password) <= 6:
            flash("password should be more than 6 characters",category="error")
        elif password!=password2:
            flash("Passwords dont match",category="error")  
        else:
            new_user=User(name=name,email=email,password=generate_password_hash(password,method='sha256'))
            db.session.add(new_user)
            db.session.commit()
          


            flash("Signed up successfully",category='success')
            return redirect("/home")    
    return render_template("signup.html")


@views.route("/logout")
@login_required
def logout():
    logout_user

    return redirect("/")



@views.route("/home",methods=['GET','POST'])
@login_required
def home():
    if request.method=='POST':
        note=request.form.get('note')
        if len(note) < 1:
            flash('note too short' , category='error')
        else:   
            new_note=Note(data=note,user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
    return render_template("todo.html",user=current_user)


@views.route('/delete/<int:id>')
def Delete(id):
    todo= Note.query.filter_by(id=id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/home")
