import os
from flask import Flask, render_template, session
from flask_session import Session
from src.utils import (
    open_waste_slot,
    close_waste_slot,
    take_trash_picture,
    process_waste,
)
from src.client import predictor


app = Flask(__name__)
SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
Session(app)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/start')
def insert():

    open_waste_slot()
    session['image_uri'] = take_trash_picture()

    return render_template('insert.html', file=session['image_uri'])


@app.route('/waste/pick-type')
def pick_type():
    close_waste_slot()
    image_uri = session.get('image_uri')
    with open(
        str(os.path.join("./camera", image_uri)), "rb"
    ) as image_contents:
        results = predictor.classify_image(
            "22b0f2f0-d422-43d3-8682-2d7944d016ae",
            "Iteration1",
            image_contents.read())

    map = {
        'bottles': 'une bouteille en plastique',
        'cutlery': 'des couverts en plastique',
        'glass': 'un gobelet en plastique'
    }

    tag_name = map[results.predictions[0].tag_name]
    proba = '{:.2f}%'.format(results.predictions[0].probability * 100)

    data = {
        'image': image_uri,
        'tag_name': tag_name,
        'proba': proba
    }
    session['waste_type'] = results.predictions[0].tag_name
    return render_template('type.html', data=data)


@app.route('/confirmation')
def confirmation():
    waste_type = session['waste_type']
    process_waste(waste_type)
    return render_template('confirmation.html')


@app.route('/infirmation')
def infirmation():
    return render_template('infirmation.html')


if __name__ == "__main__":
    app.run(debug=True)
