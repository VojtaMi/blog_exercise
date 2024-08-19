from flask_wtf import FlaskForm
from werkzeug.security import check_password_hash
from wtforms import StringField, SubmitField, EmailField, PasswordField
from wtforms.validators import DataRequired, URL, Length, Email, ValidationError
from flask_ckeditor import CKEditorField
import zxcvbn
import crud


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


email_validators = [
    DataRequired(message="Email is required."),
    Email(message="Please provide a valid email address."),  # Ensures correct format
    Length(max=100, message="Email cannot exceed 100 characters.")
]
password_validators = [
    DataRequired(message="Password is required."),
    Length(max=100, message="Password cannot exceed 100 characters.")
]


class RegisterForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[
            DataRequired(message="Username is required."),
            Length(max=100, message="Username cannot exceed 100 characters.")
        ]
    )

    email = EmailField(
        "Email",
        validators=[
            DataRequired(message="Email is required."),
            Email(message="Please provide a valid email address."),
            Length(max=100, message="Email cannot exceed 100 characters.")
        ]
    )

    password = PasswordField(
        "Password",
        validators=password_validators,
    )

    def validate_password(self, field):
        result = zxcvbn.zxcvbn(field.data)
        if result['score'] < 3:
            raise ValidationError(
                "Password is too weak. Suggestions: " + ", ".join(result['feedback']['suggestions']))

    submit = SubmitField("Register")


from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, ValidationError
from werkzeug.security import check_password_hash
from your_app import crud  # Adjust import according to your project structure

class LoginForm(FlaskForm):
    email = EmailField(
        "Email",
        validators=[
            DataRequired(message="Email is required."),
            Email(message="Please provide a valid email address."),
            Length(max=100, message="Email cannot exceed 100 characters.")
        ]
    )

    password = PasswordField(
        "Password",
        validators=[
            DataRequired(message="Password is required."),
            Length(max=100, message="Password cannot exceed 100 characters.")
        ]
    )

    def validate_email(self, field):
        """Check if the email exists in the database and store the user."""
        self.user = crud.get_user_by_email(field.data)
        if not self.user:
            raise ValidationError("No account found with this email address.")

    def validate_password(self, field):
        """Check if the password matches the hashed password."""
        if hasattr(self, 'user'):
            if not check_password_hash(self.user.password, field.data):
                raise ValidationError("Incorrect password. Please try again.")

    submit = SubmitField("Login")
