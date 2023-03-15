from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class PostForm(FlaskForm):
      title = StringField("Title:", validators=[DataRequired()])
      link = StringField("Link:", validators=[DataRequired()])
      submit = SubmitField("Post")

