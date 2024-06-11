from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)

@app.route('/')
def home():
    filter_option = request.args.get('filter', 'all')
    if filter_option == 'completed':
        tasks = Task.query.filter_by(completed=True).all()
    elif filter_option == 'not_completed':
        tasks = Task.query.filter_by(completed=False).all()
    else:
        tasks = Task.query.all()
    return render_template('index.html', tasks=tasks, filter_option=filter_option)

@app.route('/add', methods=['POST'])
def add_task():
    task_content = request.form.get('task')
    if task_content:
        new_task = Task(content=task_content)
        db.session.add(new_task)
        db.session.commit()
    return redirect(url_for('home'))

@app.route('/delete/<int:id>')
def delete_task(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/edit/<int:id>', methods=['POST'])
def edit_task(id):
    task = Task.query.get_or_404(id)
    new_content = request.form.get('task')
    if new_content:
        task.content = new_content
        db.session.commit()
    return redirect(url_for('home'))

@app.route('/toggle/<int:id>')
def toggle_task(id):
    task = Task.query.get_or_404(id)
    task.completed = not task.completed
    db.session.commit()
    return redirect(url_for('home'))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=8000)