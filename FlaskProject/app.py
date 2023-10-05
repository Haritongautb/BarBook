from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flaskProject.db'
db = SQLAlchemy(app)

app.debug = True
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)

class DeleteAll(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)


@app.route("/index")
@app.route("/")
def index():
    pageTitle = "<h2>Это title 2</h2>"
    return render_template("index.html", pageTitle=pageTitle)


@app.route("/about")
def about():
    return render_template("about.html")


# Отличие между GET и POST
# Метод POST используется для отправки данных на сервер.
# Метод GET используется для запроса информации с сервера. Данные, отправляемые с помощью метода GET, добавляются к URL-адресу и становятся видимыми для всех.
# При отправке этой формы, браузер сформирует URL-адрес с добавленными параметрами, например: /search?query=example.
@app.route("/posts", methods=['GET'])
def posts():
    if request.method == "GET" and "id" in request.args:
        print(request.args)
        print("Это id")
        post_id = request.args['id']
        post = Post.query.get(post_id)
        print(post)
        return render_template("/posts.html", posts=[post])
        # Для избежания автоматической отработки POST при перезагружки страницы, в браузере это по дефолту, бразуер сам делает запрос POST при перезагрузки страницы
        # return redirect(url_for('posts'))
    else:
        posts = Post.query.all()
        return render_template("/posts.html", posts=posts)


# Отличие между GET и POST
# Метод POST используется для отправки данных на сервер.
# Метод GET используется для запроса информации с сервера. Данные, отправляемые с помощью метода GET, добавляются к URL-адресу и становятся видимыми для всех.
# При отправке этой формы, браузер сформирует URL-адрес с добавленными параметрами, например: /search?query=example.
@app.route("/create", methods=['POST', 'GET'])
# GET - значит страница будет принимать данные и обрабатывать его
# POST - значит, что страница будет присылать данные
# Поэтому мы и пишем и GET и POST, а не только 1 POST
def create():
    if request.method == "POST":
        formTitle = request.form['title']
        formText = request.form['text']

        # Записываем запись в базу данных
        # try и except пишем, потому что в Flask может появиться ошибка при работе с базой данных
        post = Post(title=formTitle, text=formText)
        try:
            db.session.add(post)
            db.session.commit()
            return redirect("/create")
        except:
            return 'При добавлении статьи произошла ошибка!'
    else:
        print("Здесь")
        return render_template("/create.html")

@app.route("/postsJSON")
def postsJSON():
    return render_template("postsJSON.html")

@app.route("/createByJSON", methods=['POST'])
def createByJSON():
    if request.method == 'POST' and request.is_json:
        try:
            print(request.get_json())
            data = request.get_json()
            if 'title' in data and 'text' in data:
                post = Post(title=data['title'], text=data['text'])
                db.session.add(post)
                db.session.commit()
                response_data = {'message': 'Данные успешно добавлены в базу данных', "data": data}
                return jsonify(response_data), 200
            else:
                error_message = {'error': 'Отсутствуют обязательные поля "title" и "text" в JSON данных'}
                return jsonify(error_message), 400
        except Exception as e:
            error_message = {'error': 'Произошла ошибка', 'details': str(e)}
            return jsonify(error_message), 500
    else:
        return 'Метод запроса не поддерживается', 405


@app.route("/deleteAll", methods=['POST'])
def deleteAll():
    try:
        # Получаем JSON-данные с массивом айдишников из запроса
        data = request.json
        print(data)
        # Проверяем, что массив айдишников существует
        if 'ids' in data:
            # Создаем объект сессии
            session = db.session
            print("here")
            # Перебираем айдишники и удаляем соответствующие записи из базы данных
            for id_to_delete in data['ids']:
                record_to_delete = session.get(DeleteAll, int(id_to_delete))
                print(record_to_delete)
                if record_to_delete:
                    session.delete(record_to_delete)

            # Применяем изменения
            session.commit()

            return jsonify({'message': 'Записи успешно удалены'}), 200
        else:
            return jsonify({'message': 'Отсутствует массив айдишников'}), 400
    except Exception as e:
        return jsonify({'error': 'Произошла ошибка', 'details': str(e)}), 500



if __name__ == "__main__":
    app.run(debug=True)


# Using DB
# from flask import Flask, jsonify
# from flask_sqlalchemy import SQLAlchemy
#
# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'  # Замените на свой путь к базе данных
# db = SQLAlchemy(app)

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#
#     def __init__(self, username, email):
#         self.username = username
#         self.email = email
# @app.route('/api/users', methods=['GET'])
# def get_users():
#     users = User.query.all()
#     user_list = [{"id": user.id, "username": user.username, "email": user.email} for user in users]
#     return jsonify(user_list)


# Simple exampple of using return JSON
# from flask import Flask, render_template, jsonify, request
#
# app = Flask(__name__)
#
# @app.route('/get_json_data', methods=['GET'])
# def get_json_data():
#     data = {"name": "John", "age": 30}
#     return jsonify(data)
#
# @app.route("/about")
# def about():
#     return render_template("about.html")
#
# if __name__ == "__main__":
#     app.run(debug=True)


