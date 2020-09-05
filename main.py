import logging
from bson import ObjectId
from datetime import datetime
from flask import render_template, Flask, abort, request, redirect, url_for
from flask_api import FlaskAPI
from operations import Operations
# from pymongo import MongoClient

app = FlaskAPI(__name__)
logging.getLogger().setLevel(logging.DEBUG)

@app.route('/')
def home():
    return redirect(url_for('tasks'))


@app.route('/api/tasks/<task_id>', methods=['GET', 'DELETE'])
def task_details(task_id):
    if request.method == 'GET':
        return Operations().find_by(task_id)
    elif request.method == 'DELETE':
        return Operations().delete(task_id)


@app.route('/api/tasks', methods=['GET', 'POST', 'PUT'])
def tasks():
    if request.method == 'GET':
        return Operations().find()
    elif request.method == 'POST':
        if type(request.data) == list:
            return "Testing", 200  #TODO
        return Operations().insert(request.data)
    elif request.method == 'PUT':
        return Operations().update(request.data)


@app.errorhandler(404)
def handle_404(exception):
    return {'message': 'Error: Resource not found.'}, 404


@app.errorhandler(500)
def handle_404(exception):
    return {'message': 'Please contact the administrator.'}, 500


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
