from flask import Flask, render_template, session, redirect, url_for, session, flash
from flask_wtf import FlaskForm
from wtforms import (StringField, BooleanField, DateTimeField,
                     RadioField,SelectField,TextField,
                     TextAreaField,SubmitField)
from wtforms.validators import DataRequired
from new_web import app

app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysecretkey'

class ins_request(FlaskForm):
    '''
    This general class gets a lot of form about puppies.
    Mainly a way to go through many of the WTForms Fields.
    '''
    ins = StringField('What breed are you?')
    submit = SubmitField('Submit')







