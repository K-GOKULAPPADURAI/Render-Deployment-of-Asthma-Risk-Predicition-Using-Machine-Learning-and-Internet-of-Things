from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import FloatField, SubmitField
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import joblib


app = Flask(__name__)
app.config['SECRET_KEY'] = b'\x05\xa2\xe3\xd4\xa3\xd6m\xa4\x9c\x12\x8e\x1e\xdfm\xc5Y\xe9\x92Q\x06\xd4~\x15'

# Load the pre-trained model
model = joblib.load('decision_tree_model.joblib')

class InputForm(FlaskForm):
    username = FloatField('Enter Gender 1-Male 0-Female:', render_kw={'placeholder': 'Enter Gender 1-Male 0-Female'})
    username1 = FloatField('Enter Temperature C:', render_kw={'placeholder': 'Enter Temperature C'})
    username2 = FloatField('Enter Humidity %:', render_kw={'placeholder': 'Enter Humidity %'})
    username3 = FloatField('Enter PM 2.5 Value:', render_kw={'placeholder': 'Enter PM 2.5 Value'})
    username4 = FloatField('Enter PM 10 Value:', render_kw={'placeholder': 'Enter PM 10 Value'})
    username5 = FloatField('Enter Actual PEFR value:', render_kw={'placeholder': 'Enter Actual PEFR value'})
    submit = SubmitField('Calculate')

def predict_risk(g, p, q, r, s):
    input_data = pd.DataFrame.from_dict({'Gender': [g], 'Outdoor Temperature': [p], 'Humidity': [q],
                                          'PM 2.5 ': [r], 'PM 10': [s]})
    prediction = model.predict(input_data)[0]
    return prediction

@app.route('/', methods=['GET', 'POST'])
def index():
    form = InputForm()
    if form.validate_on_submit():
        return render_template('result.html', form=form)
    return render_template('index.html', form=form)

@app.route('/calculate', methods=['POST'])
def calculate():
    form = InputForm(request.form)
    if form.validate():
        g = form.username.data
        p = form.username1.data
        q = form.username2.data
        r = form.username3.data
        s = form.username4.data
        actual_pefr = form.username5.data

        # Call the prediction function
        prediction_result = predict_risk(g, p, q, r, s)

        # Calculate the percentage of actual PEFR to predicted PEFR
        predicted_pefr = prediction_result
        perpefr = (actual_pefr / predicted_pefr) * 100

        # Determine risk category based on the percentage
        if perpefr >= 80:
            risk_status = 'SAFE'
            result_color = '#00FF00'
        elif perpefr >= 50:
            risk_status = 'MODERATE'
            result_color = '#FFFF00'
        else:
            risk_status = 'RISK'
            result_color = '#FF0000'

        return render_template('result.html', result=risk_status, predicted_pefr=predicted_pefr,
                               actual_pefr=actual_pefr, details="Details Here", result_color=result_color)

    return render_template('index.html', form=form)
if __name__ == '__main__':
    app.run(debug=True)
