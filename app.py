from flask import Flask, render_template, request, redirect, url_for  # type: ignore
from flask_sqlalchemy import SQLAlchemy  # type: ignore

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(app)

from models import ToDo
with app.app_context():
    db.create_all()
    
@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/tasks')
def index():
    todo_list = ToDo.query.all()
    return render_template('index.html', todo_list=todo_list)

@app.route('/add', methods=['POST'])
def add():
    task_content = request.form.get('task')
    if task_content:
        new_task = ToDo(task=task_content)
        db.session.add(new_task)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>')
def delete(task_id):
    task = ToDo.query.get(task_id)
    if task:
        db.session.delete(task)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    task = ToDo.query.get_or_404(task_id)
    if request.method == 'POST':
        new_content = request.form['task']
        if new_content:
            task.task = new_content
            db.session.commit()
            return redirect(url_for('index'))
    return render_template('edit.html', task=task)

@app.route('/toggle/<int:task_id>', methods=['POST'])
def toggle_complete(task_id):
    task = ToDo.query.get_or_404(task_id)
    task.completed = not task.completed
    db.session.commit()
    return redirect(url_for('index'))

@app.route("/update/<int:task_id>", methods=["POST"])
def update_task(task_id):
    task = ToDo.query.get(task_id)
    task.task = request.form["task"]
    db.session.commit()
    return redirect(url_for("index"))



if __name__ == '__main__':
    app.run(debug=True)
