

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import DataRequired,EqualTo
from wtforms import ValidationError
# for profile picture display
from flask_wtf.file import FileField, FileAllowed
from monitor_system.models import Organisation,Instrument


class Ogran_RegistrationForm(FlaskForm):
    organ_name = StringField('Organisation Name', validators=[DataRequired()],id="organ_name")
    organ_submit = SubmitField('Register New Organisation!',id="organ_submit")

    def check_name(self, field):

        # Check if not None for that name!
        if Organisation.query.filter_by(name=field.data).first():
            raise ValidationError('Sorry, that organisation name is taken!')

class Ins_RegistrationForm(FlaskForm):
    o_id = IntegerField('Organisation ID', validators=[DataRequired()])
    ins_name = StringField('Instrument Name', validators=[DataRequired()],id="ins_name")
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('pass_confirm', message='Passwords are not the same!')])
    pass_confirm = PasswordField('Confirm password', validators=[DataRequired()])
    ins_submit = SubmitField('Register New Instrument!',id="ins_submit")

    def validate_name(self, field):
        print ("in check name")
        # Check if not None for that name!
        if Instrument.query.filter_by(o_id=field.data,ins_name=field.data).first():
            raise ValidationError('Sorry, that instrument name is taken in this organisation!')

#
# class UpdateUserForm(FlaskForm):
#     organisation_id = IntegerField('Organisation ID', validators=[DataRequired()])
#     instrument_name = StringField('Instrument name', validators=[DataRequired()])
#     picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
#     submit = SubmitField('Update')
#
#
#     def check_username(self, field):
#         # Check if not None for that username!
#         if User.query.filter_by(username=field.data).first():
#             raise ValidationError('Sorry, that username is taken!')
