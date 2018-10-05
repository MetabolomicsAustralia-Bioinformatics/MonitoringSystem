from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from monitor_system.models import Organisation, Instrument
from wtforms import ValidationError
from wtforms.validators import DataRequired, Email, EqualTo
# for profile picture display
from flask_wtf.file import FileField, FileAllowed


class Ogran_RegistrationForm(FlaskForm):
    organ_name = StringField('Organisation Name', validators=[DataRequired()], id="organ_name")
    picture = FileField('Upload Organisation Profile Image', validators=[FileAllowed(['jpg', 'png'])])
    organ_submit = SubmitField('Register New Organisation!', id="organ_submit")

    def check_name(self, field):
        # Check if not None for that name!
        if Organisation.query.filter_by(name=field.data).first():
            raise ValidationError('Sorry, that organisation name has been taken!')


class Ins_RegistrationForm(FlaskForm):
    o_id = IntegerField('Organisation ID', validators=[DataRequired()])
    ins_name = StringField('Instrument Name', validators=[DataRequired()], id="ins_name")
    password = PasswordField('Password', validators=[DataRequired(),
                                                     EqualTo('pass_confirm', message='Passwords are not the same!')])
    pass_confirm = PasswordField('Confirm password', validators=[DataRequired()])
    ins_submit = SubmitField('Register New Instrument!', id="ins_submit")

    def validate_name(self, field):
        # Check if not None for that name!
        if Instrument.query.filter_by(o_id=field.data, ins_name=field.data).first():
            raise ValidationError('Sorry, that instrument name is taken in this organisation!')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')


class UpdateOrganisationForm(FlaskForm):
    organ_name = StringField('Organisation Name', validators=[DataRequired()], id="organ_name")
    picture = FileField('Update Organisation Profile Image', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')
