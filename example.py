from flask import Flask, render_template, request, redirect, flash, get_flashed_messages, url_for
import json
from validator import validate
import os

app = Flask(__name__)
#app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
import secrets

secret = secrets.token_urlsafe(32)

app.secret_key = secret


@app.route('/')
def hello_world():
    return 'Welcome to Flask, our dear friends!'

#@app.get('/users')
#def users_get():
#    return 'GET /users'

#@app.post('/users')
#def users():
#    return 'Users', 302

@app.route('/courses/<id>')
def courses(id):
    return f'Course id: {id}'

@app.route('/users/<id>')
def get_user(id):
    if not user:
        return 'Page not found', 404
    return render_template(
        'users/show.html',
        name=id,
        )        


@app.get('/users')
def search_users():
    #users = ['mike', 'mishel', 'adel', 'keks', 'kamila']
    messages = get_flashed_messages(with_categories=True)
    with open('data.json', 'r') as f:
        users = json.loads(f.read())
    term = request.args.get('term')
    filtered_users = []
    for user in users:
        if str(term).lower() in user['nickname'].lower():
            filtered_users.append(user)
    return render_template(
        'users/index.html',
        users=filtered_users,
        search=term,
        messages=messages,
    )


@app.route('/users/new')
def users_new():
    user = {'nickname': '',
            'email': ''}
    errors = {}
    return render_template(
        'users/new.html',
        user=user,
        errors=errors,
    )


@app.post('/users')
def users_post():
    user = request.form.to_dict()
    errors = validate(user)
    if errors:
        return render_template(
            'users/new.html',
            user=user,
            errors=errors,
            ), 422

    with open("data.json", "r") as f:
        users = json.loads(f.read())
    users.append(user)
    with open("data.json", "w") as f:
        f.write(json.dumps(users))
    
    flash('Вы добавлены успешно!', 'success')
    return redirect(url_for('search_users'), code=302)


