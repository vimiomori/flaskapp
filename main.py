import logging
from bson import ObjectId
from datetime import datetime
from flask import render_template, Flask, abort, request, redirect, url_for
from flask_api import FlaskAPI
from pymongo import MongoClient

app = FlaskAPI(__name__)
logging.getLogger().setLevel(logging.DEBUG)

@app.route('/')
def home():
    return redirect(url_for('tasks'))


def insert(data):
    with MongoClient("127.0.0.1", 27017) as client:
        db = client.todo_app
        tasks_collection = db.tasks_collection
        task = {
            "content": data['content'],
            "do_by": datetime.strptime(data['do_by'], "%m/%d/%Y"),
            "done": data['done']
        }
        result = tasks_collection.insert_one(task)
        task['_id'] = str(result.inserted_id)
        return task


def find():
    with MongoClient("127.0.0.1", 27017) as client:
        db = client.todo_app
        tasks_collection = db.tasks_collection
        tasks = []
        for task in tasks_collection.find():
            task['_id'] = str(task['_id'])
            tasks.append(task)
        return tasks


def find_by(_id):
    with MongoClient("127.0.0.1", 27017) as client:
        db = client.todo_app
        tasks_collection = db.tasks_collection
        task = tasks_collection.find_one({'_id': ObjectId(_id)})
        task['_id'] = str(task['_id'])
        return task


def update(task):
    with MongoClient("127.0.0.1", 27017) as client:
        db = client.todo_app
        tasks_collection = db.tasks_collection
        filter = {'_id': ObjectId(task['_id'])}
        update = {
            '$set': dict(list(task.items())[1:])
        }
        tasks_collection.update_one(filter, update)
        return task


def delete(_id):
    with MongoClient("127.0.0.1", 27017) as client:
        db = client.todo_app
        tasks_collection = db.tasks_collection
        filter = {'_id': ObjectId(str(_id))}
        result = tasks_collection.delete_one(filter)
        return result.deleted_count


@app.route('/api/tasks/<task_id>', methods=['GET', 'DELETE'])
def task_details(task_id):
    if request.method == 'GET':
        return find_by(task_id), 200
    elif request.method == 'DELETE':
        deleted_count = delete(task_id)
        if deleted_count != 1:
            return f"Error: Failed to delete task (id: {task_id})", 400
        return '', 204

@app.route('/api/tasks', methods=['GET', 'POST', 'PUT'])
def tasks():
    if request.method == 'GET':
        return {'tasks': find()}, 200
    elif request.method == 'POST':
        return insert(request.data), 201
    elif request.method == 'PUT':
        return update(request.data), 200


@app.errorhandler(404)
def handle_404(exception):
   return {'message': 'Error: Resource not found.'}, 404
    # return "Page not found", 404


@app.errorhandler(500)
def handle_404(exception):
   return {'message': 'Please contact the administrator.'}, 500


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
