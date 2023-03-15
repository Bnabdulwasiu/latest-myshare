from flask import (render_template, url_for, flash,
                   request, abort, redirect, Blueprint)
from flask_login import current_user, login_required
from myshare import db
from myshare.models import Link
from myshare.link_posts.forms import PostForm


link_posts = Blueprint('link_posts', __name__)

#Route where users create new posts
@link_posts.route("/post/new", methods=["GET","POST"])
@login_required
def new_post():
    form = PostForm()
    if request.method == "POST":
        title = form.title.data
        link = form.link.data
        
        if title and link:
            link_post = Link(title=title, content=link, author=current_user)
            db.session.add(link_post)
            db.session.commit()
            flash("Post has been created succesfully", category="success")
            return redirect(url_for("main.home"))
        else:
            flash("Fill all fields to submit form", category="error")
        
    return render_template("create_post.html", title="Create post",
                           legend="New post:", form=form)


#Route where users can update their posts    
@link_posts.route("/post/<int:post_id>/update", methods=["GET", "POST"])
@login_required
def update_post(post_id):
    
    link_post = Link.query.get(post_id)
    if link_post.author != current_user:
        abort(403)
    
    form = PostForm()
    if request.method == "POST":
        
        if form.title.data and form.link.data:
            
            link_post.title = form.title.data
            link_post.content = form.link.data
            db.session.commit()
            flash("Your post has been updated succesfully.", category="success")
            return redirect(url_for("link_posts.update_post", post_id=link_post.id))
    
    if request.method == "GET":
        form.title.data = link_post.title
        form.link.data = link_post.content
        
    form.title.data = link_post.title
    form.link.data = link_post.content
        
    return render_template("create_post.html", title="Update post", 
                            legend="Update Post:", link_title=link_post.title,         
                            content=link_post.content, form=form, link=link_post)


#Route to delete posts
@link_posts.route("/post/<int:post_id>/delete", methods=["POST"])
@login_required
def delete_post(post_id):
    link_post = Link.query.get_or_404(post_id)
    if link_post.author != current_user:
        abort(403)
        
    db.session.delete(link_post)
    db.session.commit()
    flash("Your post have been deleted successfully", category="success")
    return redirect(url_for("main.home"))

