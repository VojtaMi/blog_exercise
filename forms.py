from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL, Length
from flask_ckeditor import CKEditorField


class PostForm(FlaskForm):
    title = StringField("Blog Post Title",
                        validators=[DataRequired(),
                                    Length(max=250, message="Title cannot exceed 250 characters.")])

    subtitle = StringField("Subtitle",
                           validators=[DataRequired(),
                                       Length(max=250, message="Subtitle cannot exceed 250 characters.")])

    author = StringField("Your Name",
                         validators=[DataRequired(),
                                     Length(max=250, message="Author's name cannot exceed 250 characters.")])

    img_url = StringField("Background Image URL",
                          validators=[DataRequired(), URL(),
                                      Length(max=250, message="Image URL cannot exceed 250 characters.")])

    body = CKEditorField("Blog Content",
                         validators=[DataRequired()])

    submit = SubmitField("Submit")
