from flask import render_template, request, Blueprint, flash, redirect, url_for
from monitor_system import db
from monitor_system.models import Organisation, Instrument, Admin
from monitor_system.admin.forms import LoginForm, UpdateOrganisationForm
from monitor_system.admin.forms import Ogran_RegistrationForm, Ins_RegistrationForm
from flask_login import login_user, login_required, logout_user, current_user
from monitor_system.admin.picture_handler import add_pic

admin = Blueprint('admin', __name__)


@admin.route('/login', methods=['GET', 'POST'])
def login():
    try:
        user = current_user.username
        return redirect(url_for('admin.view'))
    except:
        form = LoginForm()
        if form.validate_on_submit():
            # Grab the user from our User Models table
            email = Admin.query.filter_by(email=form.email.data).first()
            # Check that the user was supplied and the password is right
            # The verify_password method comes from the User object
            # try:
            if email.check_password(form.password.data) and admin is not None:
                # Log in the user
                login_user(email)

                next = request.args.get('next')

                # So let's now check if that next exists, otherwise we'll go to
                # the welcome page.
                if next == None or not next[0] == '/':
                    next = url_for('admin.view')

                # return redirect(next)
                return redirect(next)
            else:
                flash("Incorrect Email or password.")
                flash("Please try again")

        return render_template('login.html', form=form)


@admin.route('/view')
@login_required
def view():
    all_organisations = []
    for organisation in Organisation.query.all():
        o_id = organisation.id
        o_name = organisation.name
        instruments = [instrument.name for instrument in Instrument.query.filter(Instrument.o_id == o_id).all()]
        all_organisations.append((o_id, o_name, instruments))

    return render_template('admin.html', all_organisations=all_organisations)


@admin.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    organ_form = Ogran_RegistrationForm()
    ins_form = Ins_RegistrationForm()

    if request.method == "POST":
        if ins_form.validate_on_submit():
            instrument = Instrument(o_id=ins_form.o_id.data, name=ins_form.ins_name.data,
                                    password=ins_form.password.data)

            db.session.add(instrument)
            db.session.commit()

            return redirect(url_for('admin.view'))

        elif organ_form.validate_on_submit():
            organ_name = organ_form.organ_name.data
            pic = add_pic(organ_form.picture.data, organ_name)
            organisation = Organisation(organ_name, pic)

            db.session.add(organisation)
            db.session.commit()
            return redirect(url_for('admin.view'))

    return render_template('register.html', organ_form=organ_form, ins_form=ins_form)


@login_required
@admin.route('/<o_name>', methods=['GET', 'POST'])
def organ_page(o_name):
    update_o_form = UpdateOrganisationForm()
    organisation = Organisation.query.filter(Organisation.name == o_name).first()
    count = 0
    instruments = []
    for instrument in Instrument.query.filter(Instrument.o_id == organisation.id).all():
        count += 1
        instrument = (instrument.name, count)
        instruments.append(instrument)

    # instruments = [instrument.name for instrument in Instrument.query.filter(Instrument.o_id == organisation.id).all()]

    if request.method == "POST":
        if update_o_form.validate_on_submit():

            if update_o_form.organ_name.data != o_name:
                # Check if not None for that name
                if Organisation.query.filter_by(name=update_o_form.organ_name.data).first():
                    flash('Sorry, that name has been take!')
                    o_pic = organisation.profile_image
                    organisation = (o_name, o_pic)
                    update_o_form.organ_name.data = o_name
                else:
                    organisation.name = update_o_form.organ_name.data
                    if update_o_form.picture.data:
                        pic = add_pic(update_o_form.picture.data, o_name)
                        organisation.profile_image = pic
                    db.session.commit()
                    flash('Organisation Information Updated')
                    return redirect(url_for('admin.organ_page', o_name=organisation.name))

            else:
                if update_o_form.picture.data:
                    pic = add_pic(update_o_form.picture.data, o_name)
                    organisation.profile_image = pic
                    db.session.commit()
                    flash('Organisation Information Updated')
                    return redirect(url_for('admin.organ_page', o_name=organisation.name))


    elif request.method == "GET":
        o_pic = organisation.profile_image
        o_id = organisation.id
        organisation = (o_name, o_pic, o_id)
        update_o_form.organ_name.data = o_name

    return render_template('organisation_page.html', organisation=organisation, update_o_form=update_o_form,
                           instruments=instruments)


# delete_organisation
@admin.route('/<o_name>/delete', methods=['GET', 'POST'])
@login_required
def delete_organisation(o_name):
    organisation = Organisation.query.filter(o_name == Organisation.name).first()
    db.session.delete(organisation)
    db.session.commit()
    flash('Organisation has been deleted')
    return redirect(url_for('admin.view'))


@admin.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('core.view'))
