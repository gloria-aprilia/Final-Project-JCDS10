from flask import Flask,render_template,request
import plotly
import plotly.graph_objs as go
import plotly.express as px

import pandas as pd
import numpy as np
import json
import joblib

app = Flask(__name__)


# generate dataframe
df = pd.read_csv("./static/data.csv")

# default page (distribution plot page)
@app.route('/')
def index():
    return render_template('insights.html')


# insights function
@app.route('/insights')
def insights_fn():
    return render_template('insights.html')


# data display function
@app.route('/see_the_data', methods=['POST','GET'])
def data_fn():
    if request.method == 'GET':
        return render_template('data.html')
    elif request.method == 'POST':
        disp = []
        num = int(request.form.get('num_disp'))
        source = df.sample(num).to_dict('records')
        for i in source:
            disp.append(i)
        return render_template('data.html',
                                num=num,
                                disp=disp,
                                title='Data')


# distribution plot function
def category_plot(cat_plot = 'histogram', cat_x = 'age' ):

    # jika menu yang dipilih adalah histogram
    if cat_plot == 'histogram':
        # siapkan list kosong untuk menampung konfigurasi hist
        data = []
        # generate config histogram dengan mengatur sumbu x dan sumbu y
        new_data = go.Histogram(
            x=df[:][cat_x]
        )

        data.append(new_data)
        #tentukan title dari plot yang akan ditampilkan
        title='Histogram'
    elif cat_plot == 'box':
        data = []
        new_data = go.Box(
            x = df[cat_x],
        )
       
        data.append(new_data)
        title='Box'
    # menentukan nama sumbu x dan sumbu y
    
    layout = go.Layout(
        title=title,
        xaxis=dict(title=cat_x),
        # yaxis=dict(title='Jumlah Data')
    )
    #simpan config plot dan layout pada dictionary
    result = {'data': data, 'layout': layout}

    #json.dumps akan mengenerate plot dan menyimpan hasilnya pada graphjson
    graphJSON = json.dumps(result, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON
@app.route('/distribution_plot/<nav>')
def cat_fn(nav):

    # saat klik menu navigasi
    if nav == 'True':
        cat_plot = 'histogram'
        cat_x = 'age'
    
    # saat memilih value dari form
    else:
        cat_plot = request.args.get('cat_plot')
        cat_x = request.args.get('cat_x')

    # Dropdown menu
    list_plot = [('histogram', 'Histogram'), ('box', 'Box')]
    list_x = [('waiting', 'Waiting'), ('age', 'Age')]
   
    plot = category_plot(cat_plot, cat_x)
    return render_template(
        'distribution_plot.html',
        plot=plot,
        focus_plot=cat_plot,
        focus_x=cat_x,
        drop_plot= list_plot,
        drop_x= list_x,
        title='Distribution Plot'
    )


# count plot function
def pie_plot(chart="count",feature="gender", hue = 'noshow'):
    
    if chart == "pie" :
        vcounts = df[feature].value_counts()

        labels = []
        values = []

        for item in vcounts.iteritems():
            labels.append(item[0])
            values.append(item[1])
        
        data = [
            go.Pie(
                labels=labels,
                values=values
            )
        ]

        layout = go.Layout(title='Pie', title_x= 0.5)

        result = {'data': data, 'layout': layout}

        graphJSON = json.dumps(result,cls=plotly.utils.PlotlyJSONEncoder)

        return graphJSON

    elif chart == "count":

        df[hue] = df[hue].astype('string')
        df[feature] = df[feature].astype('string')

        df1 = df[df[hue] == df[hue].unique()[0]]
        df2 = df[df[hue] == df[hue].unique()[1]]

        trace1 = go.Bar(x=df1[feature], y=df1[df[feature]== df[feature].unique()[0]].value_counts(), name=df[hue].unique()[0])
        trace2 = go.Bar(x=df2[feature], y=df2[df[feature]== df[feature].unique()[0]].value_counts(), name=df[hue].unique()[1])
        
        data = [trace1, trace2]
        # generate config Bar
        layout = go.Layout(title=f"{feature} vs {hue}",
                   xaxis=dict(title=f"{feature}"),
                   yaxis=dict(title="Value Counts"),
                   legend=dict(x=1.0, y=1),
                   # Here annotations need to create legend title
                   annotations=[
                                dict(
                                    x=1.065,
                                    y=1.05,
                                    xref="paper",
                                    yref="paper",
                                    text=hue,
                                    showarrow=False
                                )],
                   barmode="group")

        result = {'data': data, 'layout': layout}

        graphJSON = json.dumps(result, cls=plotly.utils.PlotlyJSONEncoder)

        return graphJSON
@app.route('/countplot')
def pie_fn():
    chart = request.args.get('chart')
    feature = request.args.get('feature')
    hue = request.args.get('hue')

    if chart == None:
        chart ='pie'
    if hue == None:
        hue = 'noshow'
    if feature == None:
        feature = 'gender'

    list_chart = [("count", "Count"), ("pie", "Pie")]
    list_feature = [('noshow', 'No Show'), ('sms_received', 'SMS Received'), ('scholarship', 'Scholarship'), ('diabetes', 'Diabetes'),('hypertension', 'Hypertension'),('gender', 'Gender')]
    list_hue = [('noshow', 'No Show'), ('sms_received', 'SMS Received'), ('scholarship', 'Scholarship'), ('diabetes', 'Diabetes'),('hypertension', 'Hypertension'),('gender', 'Gender')]
    
    plot = pie_plot(chart,feature,hue)
    return render_template('pie.html', 
        plot=plot,
        focus_chart=chart,
        focus_feature=feature,
        focus_hue=hue,
        drop_chart= list_chart,
        drop_feature= list_feature,
        drop_hue= list_hue,
        title='Count Plot'
    )


# prediction input function
@app.route('/predict_result', methods=['POST', 'GET'])
def predict_fn():
    return render_template('predict.html', title='Prediction Input')


# prediction result function
@app.route('/result', methods=['POST', 'GET'])
def result():
    pred = ""
    prob = ""
    waiting = ""
    age = ""
    scholarship = ""
    hypertension = ""
    diabetes = ""
    sms_received = ""
    if request.method == 'POST':
        # Untuk Predict
        #appt date
        from datetime import datetime
        appt_date = request.form.get('appt_date')
        appt_date = datetime.strptime(appt_date, '%Y-%m-%d')
        #age
        age = int(request.form.get('age'))
        age_scaled = round(age/75, 4)
        #scholarship
        scholarship = int(request.form.get('scholarship'))
        #hypertension
        hypertension = int(request.form.get('hypertension'))
        #diabetes
        diabetes = int(request.form.get('diabetes'))
        #sms_received
        sms_received = int(request.form.get('sms_received'))

        # calculate waiting time
        sched_date = datetime.today().strftime('%Y-%m-%d')
        sched_date = datetime.strptime(sched_date, '%Y-%m-%d')
        waiting = appt_date-sched_date
        waiting = waiting.days

        #predict patient
        pred = model.predict([[waiting, sms_received, scholarship, diabetes, hypertension, age_scaled]])[0].round(2)
        prob = model.predict_proba([[waiting, sms_received, scholarship, diabetes, hypertension, age_scaled]])
    return render_template('result.html',                            
                            waiting=waiting,
                            age=age,
                            scholarship=scholarship,
                            hypertension=hypertension,
                            diabetes=diabetes,
                            sms_received=sms_received,
                            noshow_pred=pred,
                            noshow_prob=prob,
                            title='Prediction Result')

if __name__ == '__main__':
    model = joblib.load('finalized_model.sav')
    app.run(debug=True)
