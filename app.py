# python3
"""
    Python Flask Rest api to store xml payload as a file

    Author : Johan Fourie
    Date : 2019/11/21
    """

from flask import Flask, request, jsonify
import xmltodict
import os
import json
from werkzeug.exceptions import HTTPException


app = Flask(__name__)

HONE_PATH = '/home'


@app.errorhandler(Exception)
def handle_error(e):
    """
    Custom Exception
    """
    code = 400
    if isinstance(e, HTTPException):
        code = e.code
    return jsonify(error=str(e)), code


def generator_path(data):
    """ Generate file path
        :param data: XML String
        :return: String
        """
    # parse xml data to dict
    try:
        content_dict = xmltodict.parse(data)
    except Exception as e:
        raise Exception('Error in XML payload')

    try:
        file_name = content_dict["Call"]["Incidents"]["Incident"]["Number"] + ".xml"
        dir_name = content_dict["Call"]["Location"]["PoliceBeat"][0:2]
        dir_path = os.path.join(HONE_PATH, dir_name)
        return dir_path, file_name

    except Exception as e:
        raise Exception('No file path in xml payload')


def file_write(data, path):
    """ Store xml data to file
        :param data: data
        :param path: file path
        :return: if success, code 200
        """
    if data:
        # Write data to file
        with open(path, "w", newline='') as fw:
            fw.write(data.decode('utf8'))
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
    else:
        raise Exception('Payload is Empty')


@app.route("/", methods=['POST'])
def index():
    """Index Route
       """
    # Get xml data from request
    data = request.data

    # Get file path for saving data
    dir_path, file_name = generator_path(data)

    # Create directory for file
    if not os.path.isdir(dir_path):
        os.makedirs(dir_path)

    # create file path for saving
    save_path = os.path.join(dir_path, file_name)

    # Write data on the file path generated above
    return file_write(data, save_path)


if __name__ == "__main__":
    app.run(debug=True)
