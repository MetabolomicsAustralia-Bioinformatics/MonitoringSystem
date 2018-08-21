from flask import render_template,request,Blueprint,flash, redirect, url_for
from monitor_system import db
from monitor_system.models import Organisation,Instrument
import time
from collections import defaultdict
import datetime
from monitor_system.admin.forms import Ogran_RegistrationForm,Ins_RegistrationForm


admin = Blueprint('admin',__name__)



@admin.route('/')
def index():
    all_organisations = []
    for organisation in Organisation.query.all():
        o_id = organisation.id
        o_name = organisation.name
        instruments = [instrument.name for instrument in Instrument.query.filter(Instrument.o_id==o_id).all()]
        all_organisations.append((o_id, o_name, instruments))

    # all_organisations = {(organisation.id,organisation.name) for organisation in Organisation.query.all()}
    print(all_organisations)
    return render_template('admin.html', all_organisations=all_organisations)


@admin.route('/register', methods=['GET', 'POST'])
def register():

    organ_form = Ogran_RegistrationForm()
    ins_form = Ins_RegistrationForm()

    if request.method == "POST":
        if ins_form.validate_on_submit():
            instrument = Instrument(o_id=ins_form.o_id.data, name=ins_form.ins_name.data, password=ins_form.password.data)

            db.session.add(instrument)
            db.session.commit()
            flash("success!   registered new instruments! ")
            return redirect(url_for('admin.index'))

        elif organ_form.validate_on_submit():
            organisation = Organisation(name=organ_form.organ_name.data)

            db.session.add(organisation)
            db.session.commit()
            flash("success!   registered new organisation! ")
            return redirect(url_for('admin.index'))


    return render_template('register.html', organ_form=organ_form, ins_form=ins_form)
