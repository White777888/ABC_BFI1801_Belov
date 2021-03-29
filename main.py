#импортирт библиотек и отдельных их элементов
#импорт класса Flask, который организует работу прилоежния
#render_template - это метод, который отрисовывает переданный ему шаблон (файл html)
#request - это объект запроса, который информацию о текущем запросе
#redirect - метод, который позволяет перенаправить приложение на другую страницу
from flask import Flask, render_template, request, redirect

#импорт класса SQLAlchemy, который позволит работать с базами данных
from flask_sqlalchemy import SQLAlchemy

#from datetime import datetime

#Объявление экземпляра класса Flask
#__name__ - это название пакета, то есть группы файлов
#это имя нужно для того, чтобы Flask знал, где искать разные файлы (статические файлы, шаблоны и т.д.)
app = Flask(__name__)

#Приложению нужно указать с какой БД и как ей нужно работать
#Для установки параметра нужно обратиться к настройкам БД через ключSQLALCHEMY_DATABASE_URI
#и указать что работа будет с sqlite по адресу /Teacher.db (то есть в папке проекта)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Teacher.db'

#В Flask-SQLAlchemy есть своя система уведомления о событиях.
#Для этого он отслеживает изменения в сеансе SQLAlchemy.
#Это требует дополнительных ресурсов, поэтому лучше пока его отключить через SQLALCHEMY_TRACK_MODIFICATIONS
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#Создание объекта, через который можно будет общаться с БД
db = SQLAlchemy(app)

#db.Model - объект, представляющий таблицу БД
#В данном случае class Teacher наследуется от db.Model, благодаря чему создается новая таблица в БД
class Teacher(db.Model):
    #Это атрибуты класса, которые являются столбцами в таблице
    #db.Column() создает столбец, которому задается тип данных и другие ограничения
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    subj = db.Column(db.String(150), nullable=True)
    day = db.Column(db.String(150), nullable=True)
    time = db.Column(db.String(150), nullable=True)
    weektype = db.Column(db.Integer, nullable=False)

    #Метод __repr__ возвращает некоторое представление объекта в каком-то формате
    #В данном случае возвращает строку с именем класса объекта и его id
    #self это перменная (или указатель) для обращения объекта к самому себе
    #self.id - это обращение к своему конкретному id
    def __repr__(self):
        return "<Article %r>" % self.id


class Subj(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    s_name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return "<Subj %r>" % self.id

class TeachName(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    t_name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return "<Teacher %r>" % self.id


@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html")

@app.route('/about')
def about():
    #render_template() - это метод для обработки и отображения файла html
    #Здесь выводится файл about.html
    return render_template("about.html")

#Обработка страницы может прроисходить в разных режимах
#и одни из них POST и GET.
#В данном случае route() получил аргементы, которые говорят о том, что обработка будет происходить в POST и GET
@app.route('/create-teacher', methods=['POST', 'GET'])
def create_teacher():
    # request содержит информацию о текущем запросе и через него можно определить, что сейчас происходит
    # GET - мы посылаем пользователю что-то (показываем страницу)
    # POST - пользователь послал нам что-то на сервер
    if request.method == "POST":
        #Так же request ссодерижт информацию, отправленную пользователем через HTML-форму
        #Получить информацию можно так: request.form['имя объекта формы, через который пользовтаель вводил информацию']
        name = request.form['name']
        subj = request.form['subj']
        day = request.form['day']
        time = request.form['time']
        weektype = request.form['subjType']

        #Создание объекта класса Teacher для добавления в БД (вызов конструктора)
        teacher = Teacher(name=name, subj=subj, day=day, time=time, weektype=weektype)

        #Блок try-execption используется для перехвата ошибок
        #Если в блоке try происходит ошибка, то она перехватывается одним из блоков exception
        #В exception можно указывать конкретные типы исключений для поимки
        #Но если там ничего не указано, то оно будет ловить вообще все исключения
        try:
            #Добавление через db в рамках текущей сессии в БД объекта teacher
            db.session.add(teacher)
            #Сохранение изменений
            db.session.commit()
            #Перенаправление на другую страницу
            return redirect('/create-teacher')
        except:
            return "Произошла ошибка"
    else:
        #Если мы здесь, значит режим работы страницы GET и нужно просто что-то послать клиенту

        #Обращение к таблице Subj с запросом(query), который отсортируется по Subj.s_name (order_by) и вернет все в форме списка с помощью метода all()
        subjects = Subj.query.order_by(Subj.s_name).all()
        teachers = TeachName.query.order_by(TeachName.t_name).all()

        #Отображение файла create-teacher.html, которому передаются списки предметов и преподавателей для отображения
        return render_template("create-teacher.html", subjects=subjects, teachers=teachers)

@app.route('/teacher')
def teachers():
    teachers = Teacher.query.order_by(Teacher.name).all()
    return render_template("teacher.html", teachers=teachers)

@app.route('/teacher/<int:id>')
def teacher_detail(id):
    #Возаращение обного объекта класса Teacher с помощью метода get(), который находит запись по первичному ключу (id)
    teacher = Teacher.query.get(id)
    return render_template("teacher_detail.html", teacher=teacher)

#Строка с параметрами
#В зависимости от того, что будет на месте name и id, то будет передано в user()
#и уже непосредственно использовано для работы
@app.route('/user/<string:name>/<int:id>')
def user(name, id):
    return "User page: Hello, " + name + ' - ' + str(id)

#Функция обработки страницы с предметами
@app.route('/Subject', methods=['POST', 'GET'])
def Subject():
    if request.method == "POST":
        #Здесь добавляем что-то, если клиент что-то прислал
        s_name = request.form['subj']

        if(s_name == ""):
            return "Произошла ошибка"

        subject = Subj(s_name = s_name)
        try:
            db.session.add(subject)
            db.session.commit()
            return redirect('/Subject')
        except:
            return "Произошла ошибка"
    else:
        #Здесь просто выводим список предметов
        subjects = Subj.query.order_by(Subj.s_name).all()
        return render_template("subj.html", subjects=subjects)

@app.route('/TeachName', methods=['POST', 'GET'])
def Teachname():
    if request.method == "POST":
        #Добавляем преподавателя
        t_name = request.form['t_name']

        if (t_name == ""):
            return "Произошла ошибка"

        teacher = TeachName(t_name = t_name)
        try:
            db.session.add(teacher)
            db.session.commit()
            return redirect('/TeachName')
        except:
            return "Произошла ошибка"
    else:
        #Выводим список преподавателей
        teachers = TeachName.query.order_by(TeachName.t_name).all()
        return render_template("TeachName.html", teachers=teachers)

#Функция-декоратор это надстройка над некоторой другой функцией
#То есть, можно менять поведение функции-декораторо передавая ей разные функции
#app.route() - это метод для связки адреса страницы (/Schedule) с функцией обработки (Schedule())
#То есть, route() реализует свои методы обработки вокруг передаваемой ей функции
@app.route('/Schedule')
def Schedule():
    teachers = Teacher.query.all()
    return render_template("schedule.html", teachers=teachers)

#__name__ содержит имя запущенного модуля
#Таким образом, данное условие выполнится,
#только если файл main.py будет запущен как основная программа
if __name__ == "__main__":
    #Запуск приложения через метод run()
    app.run(debug=True)
    #debug = True включает режим отладки для приложения
    #Без него в, случае ошибки, для повторного запуска исправленного кода
    #потребуется остановить сервер и запустить сначала.
    #Если режим отладки включен, после исправления кода страницу нужно просто обновить