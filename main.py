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


# def insert(data):
#     with MongoClient("127.0.0.1", 27017) as client:
#         db = client.todo_app
#         tasks_collection = db.tasks_collection
#         task = {
#             "content": data['content'],
#             "do_by": datetime.strptime(data['do_by'], "%m/%d/%Y"),
#             "done": data['done']
#         }
#         result = tasks_collection.insert_one(task)
#         task['_id'] = str(result.inserted_id)
#         return task


# def find():
#     with MongoClient("127.0.0.1", 27017) as client:
#         db = client.todo_app
#         tasks_collection = db.tasks_collection
#         tasks = []
#         for task in tasks_collection.find():
#             task['_id'] = str(task['_id'])
#             tasks.append(task)
#         return tasks


# def find_by(_id):
#     with MongoClient("127.0.0.1", 27017) as client:
#         db = client.todo_app
#         tasks_collection = db.tasks_collection
#         task = tasks_collection.find_one({'_id': ObjectId(_id)})
#         task['_id'] = str(task['_id'])
#         return task


# def update(task):
#     with MongoClient("127.0.0.1", 27017) as client:
#         db = client.todo_app
#         tasks_collection = db.tasks_collection
#         filter = {'_id': ObjectId(task['_id'])}
#         update = {
#             '$set': dict(list(task.items())[1:])
#         }
#         result = tasks_collection.update_one(filter, update)
#         return result.modified_count, task


# def delete(_id):
#     with MongoClient("127.0.0.1", 27017) as client:
#         db = client.todo_app
#         tasks_collection = db.tasks_collection
#         filter = {'_id': ObjectId(str(_id))}
#         result = tasks_collection.delete_one(filter)
#         return result.deleted_count


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
        # return insert(request.data), 201
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
