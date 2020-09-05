import logging
from datetime import datetime
from bson import ObjectId
from pymongo import MongoClient


logging.getLogger().setLevel(logging.DEBUG)

class Operations:

    def __init__(self):
        self.client = MongoClient("127.0.0.1", 27017)
        self.db = self.client.todo_app
        self.tasks_collection = self.db.tasks_collection
    
    def insert(self, data):
        if type(data) == list:
            if not all([self.is_validate(d) for d in data]):
                return f"JSON is invalid", 400
            return self._insert_many(data)

        if not (self.is_validate(data)):
            return f"JSON is invalid", 400
        return self._insert_one(data)

    def find(self):
        tasks = []
        for task in self.tasks_collection.find():
            task['_id'] = str(task['_id'])
            tasks.append(task)
        self.client.close()
        return {'tasks': tasks}, 200

    def find_by(self, _id):
        task = self.tasks_collection.find_one({'_id': ObjectId(_id)})
        task['_id'] = str(task['_id'])
        self.client.close()
        return task, 200

    def update(self, task):
        if not (self.is_validate(task)):
            return f"JSON is invalid", 400

        if task.get('do_by'):
            task['do_by'] = self._convert_time(task['do_by'])

        update = {
            '$set': dict(list(task.items())[1:])
        }
        filter = {'_id': ObjectId(task['_id'])}
        result = self.tasks_collection.update_one(filter, update)
        self.client.close()
        if result.modified_count != 1:
            return f"Error: Failed to update task (id: {task['_id']}", 400
        return task, 200

    def delete(self, _id):
        filter = {'_id': ObjectId(str(_id))}
        result = self.tasks_collection.delete_one(filter)
        self.client.close()
        if result.deleted_count != 1:
            return f"Error: Failed to delete task (id: {_id})", 400
        return '', 204

    def _insert_many(self, data):
        tasks = [self._make_task(d) for d in data]
        result = self.tasks_collection.insert_many(tasks)
        for i, task in enumerate(tasks):
            task['_id'] = str(result.inserted_ids[i])
        self.client.close()
        return {'tasks': tasks}, 200
    
    def _insert_one(self, data):
        task = self._make_task(data)
        result = self.tasks_collection.insert_one(task)
        task['_id'] = str(result.inserted_id)
        self.client.close()
        return task, 200
    
    def _make_task(self, data):
        return {
            "content": data['content'],
            "do_by": self._convert_time(data['do_by']),
            "done": data['done']
        }

    @staticmethod
    def is_validate(data):
        for key in data.keys():
            if key not in ['_id', 'content', 'do_by', 'done']:
                return False
        return True

    @staticmethod
    def _convert_time(date):
        return datetime.strptime(date, "%m/%d/%Y")
