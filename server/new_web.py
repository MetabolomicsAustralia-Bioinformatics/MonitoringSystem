from flask import Flask, render_template, request, session, redirect,url_for
from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy.orm import scoped_session, sessionmaker, Query
# from flask import Flask,redirect,url_for
import json
import time
from collections import defaultdict
import datetime
import pymysql
from models import Instrument, Sample, db, app

pymysql.install_as_MySQLdb()

app.config['SECRET_KEY'] = 'mysecretkey'
# from datetime import datetime
# app = Flask(__name__)
# # config information to connect to the database, other database could also be accepted
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:1025@localhost:3306/demo'
# # don't track all modifications
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


class Info(db.Model):
    __table__ = db.Model.metadata.tables['samples']

#homepage
@app.route('/')
def home():
    #if search_text == some_organisation
    #then redirect to the data page

    return render_template("home.html")


@app.route('/detail', methods=['POST', 'GET'])
def detail():
    ##get instrument name from DB
    all_instruments = [instrument.name for instrument in Instrument.query.all()]
    # if request.method == 'GET':
    #     print (request.args.get('sele'))
    if request.args.get('sele'):
        selected_ins = request.args.get('sele')
        print (selected_ins)
        ins_samples = Sample.query.filter_by(instrument=selected_ins).all()
        # current time
        ins_samples = ins_samples
        ct = datetime.datetime.now()
        ct = int(time.mktime(ct.timetuple()) * 1000 + ct.microsecond / 1000)
        print (len(ins_samples))
        print ("ins_samples: " + str(ins_samples))
        print (type(ins_samples))
        ft = ins_samples[0].actual_start
        ft = datetime.datetime.strptime(ft, "%Y-%m-%d %H:%M:%S.%f")
        # ft = db.session.query(Info).first().actualstarttime
        ft = int(time.mktime(ft.timetuple()) * 1000 + ft.microsecond / 1000)
        # print (ft)
        total = ct - ft
        print('ct: ' + str(ct) + "  ft: " + str(ft))
        # print (total)
        # if date_time:
            # date_time = session['date_time']
        date_timeSent = [ft, ct]
        session['date_time'] = date_timeSent
        print ("hi!!! date_time: " + str(date_timeSent))
        count_sample = len(ins_samples)
        # if date_time:
        #     print (date_time)
            # session['date_time'] = date_time
        print("hello")
        # print (type(session['date_time']))
        # return redirect(url_for("home"))
        # return redirect(url_for('home'))
        # date_time = json.dump(date_time)
        print (date_timeSent)
        # return render_template("detail.html",date_time=date_time)

            # return render_template("detail.html", all_instruments=all_instruments, date_time=date_time)
        # return render_template("detail.html")
    # if request.method == 'POST':
    #      print ('POST!!')
    #     # session['ins_samples'] = ins_samplesw
    # if request.method == 'POST' and ins_samples:
    #     print ("get in!")
    #     # first time
    #     # print (session['ins_samples'][0])
    #     ft = ins_samples[0].actual_start
    #     ft = datetime.datetime.strptime(ft, "%Y-%m-%d %H:%M:%S.%f")
    #         # ft = db.session.query(Info).first().actualstarttime
    #     ft = int(time.mktime(ft.timetuple()) * 1000 + ft.microsecond / 1000)
    #     # print (ft)
    #     total = ct - ft
    #     print ('ct: ' + str(ct) + "  ft: " + str(ft))
    #     # print (total)
    #
    #     date_time.append((ft, ct))
    #     count_sample = len(ins_samples)

        # for sample in ins_samples:
        #     smry_instruments = defaultdict(dict)
        #     samples = {}
        #     samples1 = {}
        #     data = []
        #     total_length = 0
        #
        #     st = sample.actual_start
        #     et = sample.actual_end
        #     length = sample.length
        #     # total running time
        #     total_length += length
        #
        #     st = int(time.mktime(st.timetuple()) * 1000 + st.microsecond / 1000)
        #     et = int(time.mktime(et.timetuple()) * 1000 + et.microsecond / 1000)
        #
        #     data.append([st, 1])
        #     data.append([et, 0])

            # smry_instruments[sample]['data'] = data
        # return redirect(url_for("detail"), data_time=data_time)

    print ('ready to render_template')
    return render_template("detail.html", all_instruments=all_instruments, date_time=session['date_time'])
            # find a particular sample from the second table to get information of plots
            # sample = db.session.query(Detail).filter_by(name=i.name).all()
            # samples[i.name] = sample
            # nameTar = {}


    # if request.form['form'] == 'data':
    #         # get the start and end time user input
    #         sttime1 = request.form['starttime1']
    #         ettime1 = request.form['endtime1']
    #         sttime2 = request.form['starttime2']
    #         ettime2 = request.form['endtime2']
    #         # if user forgets to input time, use default time to return all the samples
    #         if sttime1 == '' or ettime1 == '':
    #             sttime = '1000-00-00'
    #             ettime = '3000-00-00'
    #         else:
    #             sttime = sttime1 + ' ' + sttime2
    #             ettime = ettime1 + ' ' + ettime2
    #         print(sttime)
    #         print(ettime)
    #         # use start time, end time, instrument name to filter samples
    #         info_instrument = db.session.query(Info).filter_by(instrument=selected_ins).filter(
    #             Info.actualstarttime > sttime,
    #             Info.actualendtime < ettime).all()
    #
    #     samples = {}
    #     samples1 = {}
    #     for i in info_instrument:
    #         # find a particular sample from the second table to get information of plots
    #         sample = db.session.query(Detail).filter_by(name=i.name).all()
    #         samples[i.name] = sample
    #         nameTar = {}
    #         for j in sample:
    #             data = j.data
    #             # x-axis
    #             data1 = str(data['RTs'])
    #             # format is easily used in javascript(eg. 0,1,2,3,4)
    #             data1 = data1[1:len(data1) - 1]
    #             # y-axis
    #             data2 = str(data['ints'])
    #             # format is easily used in javascript(eg. 3.45,3.46,3.46...)
    #             data2 = data2[1:len(data2) - 1]
    #             # double comma helps to split x and y without splitting other data
    #             data = data1 + ',,' + data2
    #             key = str(j.EIC)
    #             nameTar[key] = data
    #         samples1[str(i.name)] = nameTar
    #     # samples1 records plots x-y coordinates. Each sample could have multiple EIC targets.
    #     samples1 = json.dumps(samples1)
    #
    #     # user = request.form['username'];
    #     # password = request.form['password'];
    #
    #     return json.dumps({'status': 'OK', 'ins': selected_ins});



@app.route('/selectIns', methods=['POST','GET'])
def selectIns():

    # selected_ins = request.form['username']


    if request.method == 'POST':
        selected_ins = request.form.get('sele')
        print(type(selected_ins))
        if request.form['form'] == 'data':

            # get the start and end time user input
            sttime1 = request.form['starttime1']
            ettime1 = request.form['endtime1']
            sttime2 = request.form['starttime2']
            ettime2 = request.form['endtime2']
            # if user forgets to input time, use default time to return all the samples
            if sttime1 == '' or ettime1 == '':
                sttime = '1000-00-00'
                ettime = '3000-00-00'
            else:
                sttime = sttime1 + ' ' + sttime2
                ettime = ettime1 + ' ' + ettime2
            print (sttime)
            print (ettime)
                # use start time, end time, instrument name to filter samples
            info_instrument = db.session.query(Info).filter_by(instrument=selected_ins).filter(Info.actualstarttime > sttime,
                                                                                           Info.actualendtime < ettime).all()


            samples = {}
            samples1 = {}
            for i in info_instrument:
                # find a particular sample from the second table to get information of plots
                sample = db.session.query(Detail).filter_by(name=i.name).all()
                samples[i.name] = sample
                nameTar = {}
                for j in sample:
                    data = j.data
                    # x-axis
                    data1 = str(data['RTs'])
                    # format is easily used in javascript(eg. 0,1,2,3,4)
                    data1 = data1[1:len(data1) - 1]
                    # y-axis
                    data2 = str(data['ints'])
                    # format is easily used in javascript(eg. 3.45,3.46,3.46...)
                    data2 = data2[1:len(data2) - 1]
                    # double comma helps to split x and y without splitting other data
                    data = data1 + ',,' + data2
                    key = str(j.EIC)
                    nameTar[key] = data
                samples1[str(i.name)] = nameTar
        # samples1 records plots x-y coordinates. Each sample could have multiple EIC targets.
            samples1 = json.dumps(samples1)


    # user = request.form['username'];
    # password = request.form['password'];

    return json.dumps({'status': 'OK', 'ins': selected_ins});


    #############################################
    ###############result content################
    #############################################
    # smry_instruments = defaultdict(dict)
    # if request.method == 'POST':
    #     # If the flag in the form is 'summary' (Search button)
    #     if request.form['form'] == 'summary':
    #         sttime = request.form['starttime']
    #         ettime = request.form['endtime']
    #         # multiple instruments could be chose by user
    #         inst = request.form.getlist('instrument')
    #         # if user forgets choose instrument return nothing
    #         if len(inst) == 0:
    #             return render_template("summary.html", instruments=instruments, smry_instruments=smry_instruments)
    #
    #         else:
    #             for j in inst:
    #
    #                 if sttime != '' and ettime != '':
    #                     info_instrument = db.session.query(Info).filter_by(instrument=j).filter(
    #                         Info.actualstarttime > sttime, Info.actualendtime < ettime).all()
    #                     # transfer start time format
    #                     st = datetime.datetime.strptime(sttime, "%Y-%m-%d").date()
    #                     # transfer end time format
    #                     et = datetime.datetime.strptime(ettime, "%Y-%m-%d").date()
    #                     # tarnsfer time format to a 13 length integer
    #                     st = int(time.mktime(st.timetuple()) * 1000)
    #                     et = int(time.mktime(et.timetuple()) * 1000)
    #                     total = et - st
    #                 # if user forgets to choose time gap then return all the samples
    #                 else:
    #                     info_instrument = db.session.query(Info).filter_by(instrument=j).all()
    #                     ct = datetime.datetime.now()
    #                     ct = int(time.mktime(ct.timetuple()) * 1000 + ct.microsecond / 1000)
    #
    #                     ft = db.session.query(Info).first().actualstarttime
    #                     ft = int(time.mktime(ft.timetuple()) * 1000 + ft.microsecond / 1000)
    #                     # the total time is from the very first sample's start time to the current time
    #                     total = ct - ft
    #
    #                 count_sample = len(info_instrument)
    #
    #                 data = []
    #                 total_length = 0
    #                 for i in info_instrument:
    #                     st = i.actualstarttime
    #                     et = i.actualendtime
    #                     length = i.length
    #                     # total running time
    #                     total_length += length
    #                     st = int(time.mktime(st.timetuple()) * 1000 + st.microsecond / 1000)
    #                     et = int(time.mktime(et.timetuple()) * 1000 + et.microsecond / 1000)
    #
    #                     data.append([st, 1])
    #                     data.append([et, 0])
    #
    #                 ratio = round(total_length * 1000 / total * 100, 2)
    #                 rest_ratio = 100 - ratio
    #                 smry_instruments[j]['count'] = count_sample
    #                 smry_instruments[j]['hours'] = round(total / 3600000, 2)
    #                 smry_instruments[j]['ratio'] = ratio
    #                 smry_instruments[j]['rest_ratio'] = rest_ratio
    #                 smry_instruments[j]['data'] = data
    #                 # smry_insruments = json.dumps(smry_instruments)

            # return render_template("summary.html", smry_instruments=smry_instruments, instruments=instruments,
            #                        inst=inst)
    # return render_template("summary.html", instruments=instruments, smry_instruments=smry_instruments)


if __name__ == '__main__':
    print('app.run??')
    app.run(debug=True)
    print ('app.run!!')
    # ft = db.session.query(Info).first().actualstarttime
    # print(ft)
    # ft = int(time.mktime(ft.timetuple()) * 1000 + ft.microsecond / 1000)
    # print(ft)
