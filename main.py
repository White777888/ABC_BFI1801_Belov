from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Teacher.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)



class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    subj = db.Column(db.String(150), nullable=True)
    inter = db.Column(db.String(150), nullable=True)

    """
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    """

    def __repr__(self):
        return "<Article %r>" % self.id

@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/create-teacher', methods=['POST', 'GET'])
def create_teacher():
    if request.method == "POST":
        name = request.form['name']
        subj = request.form['subj']
        inter = request.form['inter']

        teacher = Teacher(name=name, subj=subj, inter=inter)
        try:
            db.session.add(teacher)
            db.session.commit()
            return redirect('/teacher')
        except:
            return "Произошла ошибка"
    else:
        return render_template("create-teacher.html")

@app.route('/teacher')
def teachers():
    teachers = Teacher.query.order_by(Teacher.name).all()
    return render_template("teacher.html", teachers=teachers)

@app.route('/teacher/<int:id>')
def teacher_detail(id):
    teacher = Teacher.query.get(id)
    return render_template("teacher_detail.html", teacher=teacher)

#Получение данных из адреса
@app.route('/user/<string:name>/<int:id>')
def user(name, id):
    return "User page: Hello, " + name + ' - ' + str(id)



if __name__ == "__main__":
    app.run(debug = True)
