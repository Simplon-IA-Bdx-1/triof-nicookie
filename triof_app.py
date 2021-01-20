import os
from flask import Flask, render_template
from src.utils import (
    open_waste_slot,
    close_waste_slot,
    take_trash_picture,
    process_waste,
)
from src.client import predictor

IMAGE_URI = take_trash_picture()

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/start')
def insert():

    open_waste_slot()

    return render_template('insert.html', file=IMAGE_URI)


@app.route('/waste/pick-type')
def pick_type():
    close_waste_slot()
    with open(
        str(os.path.join("./camera", IMAGE_URI)), "rb"
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
        'image': IMAGE_URI,
        'tag_name': tag_name,
        'proba': proba
    }
    process_waste(results.predictions[0].tag_name)

    return render_template('type.html', data=data)


# @app.route('/confirmation', methods=['POST'])
# def confirmation():
#     waste_type = request.form['type']

#     process_waste(waste_type)
#     return render_template('confirmation.html')


if __name__ == "__main__":
    app.run(debug=True)
