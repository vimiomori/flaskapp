from bson import ObjectId
from pymongo import MongoClient


class Operations:

    def __init__(self):
        self.client = MongoClient("127.0.0.1", 27017)
        self.db = self.client.todo_app
        self.tasks_collection = self.db.tasks_collection
    
    def insert(self, data):
        task = {
            "content": data['content'],
            "do_by": datetime.strptime(data['do_by'], "%m/%d/%Y"),
            "done": data['done']
        }
        result = self.tasks_collection.insert_one(task)
        task['_id'] = str(result.inserted_id)
        self.client.close()
        return task
    
    def find(self):
        tasks = []
        for task in self.tasks_collection.find():
            task['_id'] = str(task['_id'])
            tasks.append(task)
        self.client.close()
        return tasks

    def find_by(self, _id):
        task = self.tasks_collection.find_one({'_id': ObjectId(_id)})
        task['_id'] = str(task['_id'])
        self.client.close()
        return task

    def update(self, task):
        filter = {'_id': ObjectId(task['_id'])}
        update = {
            '$set': dict(list(task.items())[1:])
        }
        result = self.tasks_collection.update_one(filter, update)
        self.client.close()
        return result.modified_count, task

    def delete(self, _id):
        filter = {'_id': ObjectId(str(_id))}
        result = self.tasks_collection.delete_one(filter)
        self.client.close()
        return result.deleted_count
