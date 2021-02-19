from flask import Flask, render_template, request, url_for, send_file, flash, redirect, make_response
import pickle
import numpy as np
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = '73a4b6ca8cb647a20b71423e31492452'

# For Coronavirus
with open("Coronavirus", "rb") as f:
    logisticRegression = pickle.load(f)

# For Chronic kidney disease
with open("CKD_Model", "rb") as f:
    decisionTree = pickle.load(f)

# For Heart Disease
with open("HeartDisease", "rb") as f:
    randomForest = pickle.load(f)




@app.route("/")
@app.route("/home")
def Homepage():
    # cases, cured, death = CurrentStats.currentStatus()
    return render_template("Homepage.html", feedback="False")


@app.errorhandler(404)
def page_not_found(e):
    return render_template("PageNotFound.html")

@app.route("/CKD", methods=["POST", "GET"])
def CKD():
    if request.method == "POST":
        submitted_values = request.form
        sg = str(float(submitted_values["sg"].strip()))
        albumin = str(float(submitted_values["albumin"].strip()))
        hemoglobin = str(float(submitted_values["hemoglobin"].strip()))
        pcv = str(float(submitted_values["pcv"].strip()))
        hypertension = str(float(submitted_values["hypertension"].strip()))
        sc = str(float(submitted_values["sc"].strip()))

        ckd_inputs1 = [sg, albumin, sc, hemoglobin, pcv, hypertension]
        prediction = decisionTree.predict([ckd_inputs1])
        # print("**************             ", prediction)
        if not prediction:
            return render_template("Infected.html", disease="Chronic Kidney Disease")
        else:
            return render_template("NonInfected.html")

    return render_template("ChronicKidney.html", title="Chronic Kidney Disease", navTitle="Chronic Kidney Disease", headText="Chronic Kidney Disease Detector", ImagePath="/static/Chronic_Kidney.png")


@app.route("/HeartDisease", methods=["POST", "GET"])
def Heart_disease():
    if request.method == "POST":
        # print(request.form)
        heart_dict = request.form
        age = int(heart_dict['age'])
        gender = int(heart_dict['gender'])
        height = int(heart_dict['height'])
        weight = int(heart_dict['weight'])
        sbp = int(heart_dict['sbp'])
        dbp = int(heart_dict['dbp'])
        cholestrol = int(heart_dict['cholestrol'])
        glucose = int(heart_dict['glucose'])
        smoke = int(heart_dict['smoke'])
        alcohol = int(heart_dict['alcohol'])
        active = int(heart_dict['active'])
        age = age*365
        model_input = [age, gender, height, weight, sbp,
                       dbp, cholestrol, glucose, smoke, alcohol, active]
        prediction = randomForest.predict([model_input])[0]

        if prediction:
            return render_template("Infected.html", disease="Heart Disease")
        else:
            return render_template("NonInfected.html")

    return render_template("HeartDisease.html", title="Heart Disease Detector", navTitle="Heart Disease Detector", headText="Heart Disease Probabilty Detector", ImagePath="/static/HeartPulse.png")


@app.route("/CoronavirusPrediction", methods=["POST", "GET"])
def Coronavirus():
    if request.method == "POST":
        # print(request.form)
        submitted_values = request.form
        temperature = float(submitted_values["temperature"].strip())
        age = int(submitted_values["age"])
        cough = int(submitted_values["cough"])
        cold = int(submitted_values["cold"])
        sore_throat = int(submitted_values["sore_throat"])
        body_pain = int(submitted_values["body_pain"])
        fatigue = int(submitted_values["fatigue"])
        headache = int(submitted_values["headache"])
        diarrhea = int(submitted_values["diarrhea"])
        difficult_breathing = int(submitted_values["difficult_breathing"])
        travelled14 = int(submitted_values["travelled14"])
        travel_covid = int(submitted_values["travel_covid"])
        covid_contact = int(submitted_values["covid_contact"])

        age = 2 if (age > 50 or age < 10) else 0
        temperature = 1 if temperature > 98 else 0
        difficult_breathing = 2 if difficult_breathing else 0
        travelled14 = 3 if travelled14 else 0
        travel_covid = 3 if travel_covid else 0
        covid_contact = 3 if covid_contact else 0

        model_inputs = [cough, cold, diarrhea,
                        sore_throat, body_pain, headache, temperature, difficult_breathing, fatigue, travelled14, travel_covid, covid_contact, age]
        prediction = logisticRegression.predict([model_inputs])[0]
        # print("**************             ", prediction)
        if prediction:
            return render_template("Infected.html", disease="Coronavirus")
        else:
            return render_template("NonInfected.html")

    return render_template("Coronavirus.html", title="Coronavirus Prediction", navTitle="COVID-19 Detector", headText="Coronavirus Probability Detector", ImagePath="/static/VirusImage.png")

if __name__ == '__main__':
    app.run(threaded=True, debug=True)