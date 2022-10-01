from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FormField, TextAreaField, FileField, validators
from wtforms.fields.html5 import DateField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from flask_wtf.recaptcha import RecaptchaField

SECRET_KEY = "secret"

# keys for localhost. Change as appropriate.

RECAPTCHA_PUBLIC_KEY = "6Ld23EYiAAAAADRk2HZBOMMVIc4kuQcjuqHdwzu5"
RECAPTCHA_PRIVATE_KEY = "6Ld23EYiAAAAAAWt_7rYYKPRQQ7WT3PocIR3dqbT"

# defines all forms in the application, these will be instantiated by the template,
# and the routes.py will read the values of the fields
# TODO: Add validation, maybe use wtforms.validators??
# TODO: There was some important security feature that wtforms provides, but I don't remember what; implement it

class LoginForm(FlaskForm):
    username = StringField('Username', render_kw={'placeholder': 'Username'})
    password = PasswordField('Password', render_kw={'placeholder': 'Password'})
    recaptcha = RecaptchaField()
    remember_me = BooleanField('Remember me') # TODO: It would be nice to have this feature implemented, probably by using cookies
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    first_name = StringField('First Name',[validators.Length(min=6, max=35)], render_kw={'placeholder': 'First Name'})
    last_name = StringField('Last Name', [validators.Length(min=6, max=35)], render_kw={'placeholder': 'Last Name'})
    username = StringField('Username', [validators.Length(min=4, max=25)])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm_password', message='Passwords must match')
    ])
    confirm_password = PasswordField('Repeat Password')
    recaptcha = RecaptchaField()
    submit = SubmitField('submit')


class IndexForm(FlaskForm):
    login = FormField(LoginForm)
    register = FormField(RegistrationForm)

class PostForm(FlaskForm):
    content = TextAreaField('New Post', render_kw={'placeholder': 'What are you thinking about?'})
    image = FileField('Image', validators=[FileRequired(), FileAllowed(['png', 'jpg', 'jpeg'], 'Invalid File Type. Must be  .png, .jpeg, .jpg')])
    submit = SubmitField('Post')

class CommentsForm(FlaskForm):
    comment = TextAreaField('New Comment', [validators.Length(min=6, max=200)], render_kw={'placeholder': 'What do you have to say?'})
    submit = SubmitField('Comment')

class FriendsForm(FlaskForm):
    username = StringField('Friend\'s username',[validators.Length(min=6, max=35)], render_kw={'placeholder': 'Username'})
    submit = SubmitField('Add Friend')

class ProfileForm(FlaskForm):
    education = StringField('Education', [validators.Length(min=6, max=35)],render_kw={'placeholder': 'Highest education'})
    employment = StringField('Employment',[validators.Length(min=6, max=35)], render_kw={'placeholder': 'Current employment'})
    music = StringField('Favorite song',[validators.Length(min=6, max=35)], render_kw={'placeholder': 'Favorite song'})
    movie = StringField('Favorite movie',[validators.Length(min=6, max=35)], render_kw={'placeholder': 'Favorite movie'})
    nationality = StringField('Nationality',[validators.Length(min=6, max=35)], render_kw={'placeholder': 'Your nationality'})
    birthday = DateField('Birthday')
    submit = SubmitField('Update Profile')
