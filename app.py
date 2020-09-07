from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///todo_list.db'

db = SQLAlchemy(app)

class Todo(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   text = db.Column(db.String(200))
   complete = db.Column(db.Boolean)
   date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

@app.route('/')
def index():
   page = request.args.get('page', 1, type=int)
   todos = Todo.query.order_by(Todo.date_created.desc())
   return render_template("index.html",todos=todos)

@app.route('/add',methods=['POST'])
def add():
   todo = Todo(text=request.form['todoitem'], complete=False)
   db.session.add(todo)
   db.session.commit()
   return redirect(url_for('index'))

@app.route('/complete/<int:id>', methods=['GET', 'POST'])
def complete(id):
   todo = Todo.query.filter_by(id = id).first()
   if todo:
      todo.complete = not todo.complete
      db.session.commit()
   return redirect(url_for('index'))

@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
   todo = Todo.query.filter_by(id = id).first()
   if todo:
      db.session.delete(todo)
      db.session.commit()
   return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
