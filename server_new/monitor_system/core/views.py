from flask import render_template, request, Blueprint, session
from monitor_system.models import Instrument, Sample, Organisation
import time
from collections import defaultdict
import datetime
import json
import simplejson

core = Blueprint('core', __name__)

# homepage
@core.route('/')
def index():
    all_organisations = [(organisation.name, organisation.profile_image) for organisation in Organisation.query.all()]

    return render_template("home.html", all_organisations=all_organisations)

# organisation details page
@core.route('/<o_name>')
def details(o_name):
    print(o_name)
    o_id = Organisation.query.filter(Organisation.name == o_name).first().id
    all_instruments = [instrument.name for instrument in Instrument.query.filter(Instrument.o_id == o_id).all()]
    session['all_instruments'] = all_instruments

    return render_template("details.html", all_instruments=all_instruments)

# deal with single instrument
@core.route('/singleGraph')
def singleGraph():
    if request.method == 'GET' and request.args.get('name', ''):
        selected_instrument = request.args.get('name', '')
        ins_data = defaultdict(dict)

        # if choose via date picker
        if request.args.get("start_time", None) and request.args.get("end_time", None):
            start = request.args.get('start_time')
            end = request.args.get('end_time')
            start = datetime.datetime.strptime(start, "%Y-%m-%d").date()
            end = datetime.datetime.strptime(end, "%Y-%m-%d").date()

        # if chose an span option
        elif request.args.get("span", None):

            span = request.args.get("span")

            end = datetime.datetime.now()
            # data of selected instrument in previous one day
            if span == "1day":
                start = end - datetime.timedelta(days=1)
            elif span == "1week":
                start = end - datetime.timedelta(days=7)
            elif span == "1month":
                start = end - datetime.timedelta(days=30)
            elif span == "6months":
                start = end - datetime.timedelta(days=180)
            else:
                start = end - datetime.timedelta(days=365)

        # if only pick an instrument
        # return default -- previous 1 week
        else:
            end = datetime.datetime.now()
            start = end - datetime.timedelta(days=7)

        # filter data by time and instrument
        ins_samples = Sample.query.filter(Sample.instrument == selected_instrument, Sample.actual_start <= end,
                                          Sample.actual_end >= start).all()
        end = int(time.mktime(end.timetuple()) * 1000)
        start = int(time.mktime(start.timetuple()) * 1000)

        data = []

        selected_span = end - start
        running_time = 0
        # collect the start and finish time of each running
        for sample in ins_samples:

            st = sample.actual_start
            st = int(time.mktime(st.timetuple()) * 1000)

            et = sample.actual_end

            et = int(time.mktime(et.timetuple()) * 1000)

            if st <= start:
                st = start
            if et >= end:
                et = end

            data.append([st, 1])
            data.append([et, 0])

            running_time += et - st

        uptime_hours = round(running_time / 3600000, 2)
        downtime_hours = round((selected_span - running_time) / 3600000, 2)
        ins_data['uptime'] = uptime_hours
        ins_data['downtime'] = downtime_hours
        ins_data['data'] = data

        return render_template('graph.html', start_time=start, end_time=end, ins_data=ins_data,
                               selected_instrument=selected_instrument)


# deal with multiple instruments with default span
@core.route('/defaultMultiGraph')
def defaultMultiGraph():
    if request.method == 'GET' and request.args.get('selected_instruments', ''):
        selected_instruments = request.args.get('selected_instruments', '')

        selected_instruments = json.loads(selected_instruments)
        # data of selected instruments in previous one week
        end = datetime.datetime.now()
        start = end - datetime.timedelta(days=7)

        end_int = int(time.mktime(end.timetuple()) * 1000)
        start_int = int(time.mktime(start.timetuple()) * 1000)

        info = defaultdict(dict)
        for instrument in selected_instruments:
            ins_data = defaultdict(dict)
            ins_samples = Sample.query.filter(Sample.instrument == instrument, Sample.actual_start <= end,
                                              Sample.actual_end >= start).all()
            stList = []
            etList = []
            info[instrument]["start"] = stList
            info[instrument]["end"] = etList
            running_time = 0
            if ins_samples:
                for sample in ins_samples:
                    st = sample.actual_start
                    st = int(time.mktime(st.timetuple()) * 1000)
                    et = sample.actual_end
                    et = int(time.mktime(et.timetuple()) * 1000)
                    stList.append(st)
                    etList.append(et)
                    running_time += et - st
                stList.sort()
                etList.sort()
                info[instrument]["start"] = stList
                info[instrument]["end"] = etList

            selected_span = end_int - start_int
            uptime_hours = round(running_time / 3600000, 2)
            downtime_hours = round((selected_span - running_time) / 3600000, 2)

            ratio = round(running_time / selected_span * 100, 2)

            rest_ratio = round(100 - ratio, 2)
            ins_data['uptime'] = uptime_hours
            ins_data['downtime'] = downtime_hours
            ins_data['ratio'] = ratio
            ins_data['rest_ratio'] = rest_ratio

            info[instrument]["ins_data"] = ins_data

        # transfer to string
        info = simplejson.dumps(info)
        return render_template('multiGraph.html', info=info, start_time=start_int, end_time=end_int)


@core.route('/sidebar')
def sidebar():
    if request.method == 'GET':
        all_instruments = session['all_instruments']
        mode = request.args.get('sidebar', '')
        return render_template(mode + "Sidebar" + ".html", all_instruments=all_instruments)




@core.route('/multiGraph')
def multiGraph():
    if request.method == 'GET':
        selected_instruments = request.args.get('selected_instruments', '')
        span = request.args.get("span", '')

        selected_instruments = json.loads(selected_instruments)
        if request.args.get("start_time", None) and request.args.get("end_time", None):
            start = request.args.get('start_time')
            end = request.args.get('end_time')
            start = datetime.datetime.strptime(start, "%Y-%m-%d").date()
            end = datetime.datetime.strptime(end, "%Y-%m-%d").date()

            # if chose an span option
        else:
            end = datetime.datetime.now()
            if span == "1day":
                start = end - datetime.timedelta(days=1)
            elif span == "1week":
                start = end - datetime.timedelta(days=7)
                # data of selected instrument in previous one week
            elif span == "1month":
                start = end - datetime.timedelta(days=30)
            elif span == "6months":
                start = end - datetime.timedelta(days=180)
            else:
                start = end - datetime.timedelta(days=365)

        end_int = int(time.mktime(end.timetuple()) * 1000)
        start_int = int(time.mktime(start.timetuple()) * 1000)
        info = defaultdict(dict)
        for instrument in selected_instruments:
            ins_data = defaultdict(dict)
            ins_samples = Sample.query.filter(Sample.instrument == instrument, Sample.actual_start <= end,
                                              Sample.actual_end >= start).all()
            stList = []
            etList = []
            info[instrument]["start"] = stList
            info[instrument]["end"] = etList
            running_time = 0
            if ins_samples:
                for sample in ins_samples:
                    st = sample.actual_start
                    st = int(time.mktime(st.timetuple()) * 1000)
                    et = sample.actual_end
                    et = int(time.mktime(et.timetuple()) * 1000)
                    stList.append(st)
                    etList.append(et)
                    running_time += et - st
                stList.sort()
                etList.sort()
                info[instrument]["start"] = stList
                info[instrument]["end"] = etList

            selected_span = end_int - start_int
            uptime_hours = round(running_time / 3600000, 2)
            downtime_hours = round((selected_span - running_time) / 3600000, 2)
            ratio = round(running_time / selected_span * 100, 2)
            rest_ratio = round(100 - ratio, 2)

            ins_data['uptime'] = uptime_hours
            ins_data['downtime'] = downtime_hours
            ins_data['ratio'] = ratio
            ins_data['rest_ratio'] = rest_ratio

            info[instrument]["ins_data"] = ins_data

        # transfer to string
        info = simplejson.dumps(info)

        return render_template('multiGraph.html', info=info, start_time=start_int, end_time=end_int)
