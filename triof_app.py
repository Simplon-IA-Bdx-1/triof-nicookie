import os
from flask import Flask, render_template, request
from src.utils import (
    open_waste_slot,
    close_waste_slot,
    take_trash_picture,
    process_waste,
)
from src.client import predictor


app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/start')
def insert():

    open_waste_slot()
    image_uri = take_trash_picture()

    return render_template('insert.html', file=image_uri)


@app.route('/waste/pick-type')
def pick_type():
    close_waste_slot()
    image_uri = request.args.get('uri')
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
    return render_template('type.html', data=data)


@app.route('/confirmation')
def confirmation():
    waste_type = request.args.get('waste_type')
    antimap = {
        'une bouteille en plastique': 'bottles',
        'des couverts en plastique': 'cutlery',
        'un gobelet en plastique': 'glass'
    }

    process_waste(antimap[waste_type])
    return render_template('confirmation.html')


@app.route('/infirmation')
def infirmation():
    return render_template('infirmation.html')


if __name__ == "__main__":
    app.run(debug=True)
