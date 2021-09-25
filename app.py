from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///heartfulness.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Heartfulness(db.Model):
    sno = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200), nullable = False)
    desc = db.Column(db.String(200), nullable = False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self) -> str:
        return f'{self.sno} - {self.title}'


@app.route('/', methods = ['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        form_title = request.form['title']
        form_desc = request.form['desc']
        todo = Heartfulness(title = form_title, desc = form_desc)
        db.session.add(todo)
        db.session.commit()
    allTodo = Heartfulness.query.all()
    return render_template('index.html', allTodo = allTodo)  # return 'Hello, World!'


@app.route('/update/<int:sno>', methods = ['GET', 'POST'])
def update(sno):
    if request.method == 'POST':
        update_title = request.form['title']
        update_desc = request.form['desc']
        todo = Heartfulness.query.filter_by(sno=sno).first()
        todo.title = update_title 
        todo.desc = update_desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")

    update_todo = Heartfulness.query.filter_by(sno=sno).first()
    return render_template('update.html', todo = update_todo)


@app.route('/delete/<int:sno>')
def delete(sno):
    delete_todo = Heartfulness.query.filter_by(sno=sno).first()
    db.session.delete(delete_todo)
    db.session.commit()
    return redirect("/")


if __name__ == '__main__':
    app.run(debug = True)     # port = 8000, we can change the port number too da!
