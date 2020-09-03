import logging
from datetime import datetime
from flask import render_template, Flask, abort, request
from flask_api import FlaskAPI

app = FlaskAPI(__name__)
logging.getLogger().setLevel(logging.DEBUG)

@app.route('/')
def home():
    abort(500)
    test = {
        "msg": "test",
        "status": False
    }
    message = "ToDo List"
    return render_template('index.html', message=message)


@app.route('/new_page')
def new_page():
    message = "new page"
    return render_template('new_page.html', message=message)


@app.route('/time')
def time():
    now = datetime.now()
    message = now.strftime("$Y/$m/$d %H:%M:%S")
    return render_template('new_page.html', message=message)


@app.route('/template_form', methods=['GET', 'POST'])
def template_form():
    if request.method == 'GET':
        return render_template('template_form.html')
    elif request.method == 'POST':
        return request.form['message']


@app.route('/api/tasks/<task_id>')
@app.route('/api/tasks', methods=['GET', 'POST'])
def _tasks(task_id=None):
    if request.method == 'GET':
        if task_id:
            res = {
                'id': task_id,
                'content': 'task',
                'done': False,
            }
            return res, 200
        else:
            task1 = {
                'id': 1,
                'content': 'first task',
                'done': True,
            }
            task2 = {
                'id': 2,
                'content': 'second task',
                'done': False,
            }
            task3 = {
                'id': 3,
                'content': 'third task',
                'done': False,
            }
            res = dict(task1=task1, task2=task2, task3=task3)
            return res
    elif request.method == 'POST':
        # json_data = request.get_json()
        content = request.data['content']
        res = {
            'id': 999,
            'content': content,
            'done': False,
        }
        return res, 201


@app.errorhandler(404)
def handle_404(exception):
   return {'message': 'Error: Resource not found.'}, 404
    # return "Page not found", 404


@app.errorhandler(500)
def handle_404(exception):
   return {'message': 'Please contact the administrator.'}, 500


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
