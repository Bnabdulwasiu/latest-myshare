from flask import (render_template, url_for, flash,
                   redirect, request, Blueprint)
from flask_login import (login_user, current_user, logout_user,
                         login_required)
from werkzeug.security import generate_password_hash, check_password_hash
from myshare import db
from myshare.models import User, Link
from myshare.users.forms import (RegistrationForm,
                                 LoginForm, UpdateUserAccount,
                                 RequestResetForm, ResetPasswordForm)
from myshare.users.utils import send_reset_email

users = Blueprint('users', __name__)

@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.home")) 

@users.route("/login", methods=("GET", "POST"))
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if request.method == "POST":
        email  = form.email.data
        password = form.password.data
        
        user = User.query.filter_by(email=email).first()
        
        if user:
            
            if check_password_hash(user.password, password):
                flash("Login successful!", category="success")
                login_user(user, remember=False)
                next_page = request.args.get("next")
                return redirect(next_page) if next_page else redirect(url_for("main.home"))
            
            else:
                flash("Incorrect password!", category="error") 
        else:
            flash("Email does not exist", category="error")
            
    return render_template("login.html", title="Login", form=form)

@users.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    form = RegistrationForm()
    
    if request.method == "POST":
        email = form.email.data
        user_name = form.username.data
        password = form.password.data
        confirm_password = form.confirm_password.data
        
        # Checking database to make sure no instance of user and email b4 creating a new user, for they are to be unique.
        user = User.query.filter_by(username=user_name).first()
        email_ = User.query.filter_by(email=email).first()
        
        if user:
            flash("That username is taken. Please choose another username", category="error")
        
        elif email_:
            flash("That email is taken. Please choose another email", category="error")
        ##########################################
        # Some validation checks   
        if len(user_name) < 2:
            flash("Your name should be less than 2 letters", category="error")
        elif len(password) < 7:
            flash("Password should not be less than 7 characters", category="error")
        elif password != confirm_password:
            flash("Passwords do not match", category="error")
            
        else:
            new_user = User(email=email, username=user_name, password=generate_password_hash(password, method="sha256"))
            db.session.add(new_user)
            db.session.commit()
            flash(f"Account created successsfully. Welcome {user_name.title()}", category="success")
            return redirect(url_for("users.login"))
            
            
    return render_template("sign-up.html", title="Sign up", form=form)

@users.route("/account", methods=["GET","POST"])
@login_required
def account():
    
    form = UpdateUserAccount()
    
    if request.method == "POST":
        
        if form.email.data != current_user.email or form.username.data != current_user.username:
            
            current_user.username = form.username.data
            current_user.email = form.email.data
            db.session.commit()
            flash("Your profile have been updated successfully", category="success")
            return redirect(url_for("users.account"))
         
        else:
            flash("New data should not match former data", category="error")
            
    if request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
        
    image_file = url_for("static", filename="profile_pics/" + current_user.image_file)
    return render_template("account.html", image_file=image_file, title="Account",form=form)

@users.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get("page", 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    links = Link.query.filter_by(author=user)\
            .order_by(Link.date_posted.desc())\
            .paginate(page=page, per_page=5)
    return render_template("user_posts.html", links=links, user=user)


@users.route("/reset_password", methods=['GET', "POST"])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = RequestResetForm()
    if request.method == "POST":
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_reset_email(user)
            return redirect(url_for('users.login'))
        else:
            flash("User was not found in the database, You can signup first.")
            return redirect(url_for('users.sign_up'))

    return render_template("reset_request.html", title="Reset Password", form=form)

@users.route("/reset_password/<token>", methods=['GET', "POST"])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    user = User.verify_reset_token(token)
    if user is None:
        flash("That is an invalid or expired token.", category="error")
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    
    if request.method == "POST":
        
        if form.password.data < 7:
            flash("Password should not be less than 7 characters", category="error")
        elif form.password.data != form.confirm_password.data:
            flash("Passwords do not match", category="error")
        else:
            hashed_password = generate_password_hash(form.password.data,  method="sha256")
            user.password = hashed_password
            db.session.commit()
            flash("Your password has been updated", category="success")
            return redirect(url_for("users.login"))
    # elif len(password) < 7:
    #     flash("Password should not be less than 7 characters", category="error")
    # elif password != confirm_password:
    #     flash("Passwords do not match", category="error") 
    # else:
    #     user.password = hashed_password
    #     db.session.commit()
    #     flash("Your password has been updated", category="success")
    #     return redirect(url_for("login"))
    
    return render_template('reset_token.html', title='Reset password', form=form)