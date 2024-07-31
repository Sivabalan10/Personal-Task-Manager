from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://sql12723285:jR63zqZyb2@sql12.freesqldatabase.com:3306/sql12723285'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define the user_details model
class UserDetails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.String(255), nullable=False)

# Initialize the database
with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def home():
    selected_date = request.form.get('selected_date')
    if selected_date:
        tasks = UserDetails.query.filter(UserDetails.timestamp.like(f'{selected_date}%')).all()
    else:
        today = datetime.now().strftime('%Y-%m-%d')
        tasks = UserDetails.query.filter(UserDetails.timestamp.like(f'{today}%')).all()
        selected_date = today
    total_tasks = len(tasks)
    return render_template('index.html', tasks=tasks, total_tasks=total_tasks, selected_date=selected_date)

@app.route('/add_task', methods=['POST'])
def add_task():
    task = request.form['task']
    task_date = request.form['task_date']
    task_time = request.form['task_time']
    if task and task_date and task_time:
        task_datetime = f"{task_date} {task_time}:00"
        new_task = UserDetails(task=task, timestamp=task_datetime)
        db.session.add(new_task)
        db.session.commit()
    return redirect(url_for('home'))

@app.route('/complete_task/<int:task_id>')
def complete_task(task_id):
    task = UserDetails.query.get(task_id)
    if task:
        db.session.delete(task)
        db.session.commit()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
