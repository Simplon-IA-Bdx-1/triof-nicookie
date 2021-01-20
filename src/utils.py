import os
import random
# from matplotlib.pyplot import imread


def open_waste_slot():

    """
        open the machine so that
        an user can enter the machine

    :return:
    """

    send_command_to_machine("open_waste_slot")
    return True


def close_waste_slot():
    """
    close the waste box for user safety
    :return:
    """

    send_command_to_machine("close_waste_slot")
    return True


def process_waste(waste_type):

    """
    move the good slot and shredd the waste
    :return:
    """

    move_container(waste_type)
    was_sucessful = shred_waste()

    return was_sucessful


def move_container(waste_type):

    BOTTLE_BOX = 0
    GLASS_BOX = 1
    CUTLERY_BOX = 0
    command_name = "move_container"

    if waste_type == "bottles":
        send_command_to_machine(command_name, BOTTLE_BOX)
    elif waste_type == "glass":
        send_command_to_machine(command_name, GLASS_BOX)
    elif waste_type == "cutlery":
        send_command_to_machine(command_name, CUTLERY_BOX)

    return True


def send_command_to_machine(command_name, value=None):

    """
    simulate command sending to rasberry pi
    do nothing to work even if the machine is not connected

    :param command_name:
    :param value:
    :return:
    """
    return True


def shred_waste():
    send_command_to_machine("shred_waste")

    return True


def take_trash_picture():
    """
        function simulating the picture taking
        inside the machine.

        Call this function to ask the machine to
        take picutre of the trash

        return : path of the picture
    """

    send_command_to_machine("take_picture")

    paths = os.listdir('camera')
    path = random.choice(paths)

    return str(path)


def get_top_pred(cv_result):
    """
        function that takes the return of ms custom vision call
        and select the top predited category

        return : a dictionnary of the top prdicted category
    """

    top_score = 0
    item_pred = {
        'prob': 0,
        'tag': None
    }

    map = {
        'bottles': 'une bouteille en plastique',
        'cutlery': 'des couverts en plastique',
        'glass': 'un gobelet en plastique'
    }

    for prediction in cv_result.predictions:
        if prediction.probability > top_score:
            top_score = prediction.probability
            item_pred['prob'] = '{:.2f}%'.format(prediction.probability * 100)
            item_pred['tag'] = map[prediction.tag_name]

    return item_pred
