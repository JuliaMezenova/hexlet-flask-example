from flask import Flask, render_template, request, redirect, flash, get_flashed_messages, url_for
import json

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Welcome to Flask, our dear friends!'

@app.get('/users')
def users_get():
    return 'GET /users'

@app.post('/users')
def users():
    return 'Users', 302

@app.route('/courses/<id>')
def courses(id):
    return f'Course id: {id}'

@app.route('/users/<id>')
def get_users(id):
    return render_template(
        'users/show.html',
        name=id,
    )


@app.route('/users/')
def search_users():
    users = ['mike', 'mishel', 'adel', 'keks', 'kamila']
    term = request.args.get('term')
    filtered_users = []
    for user in users:
        if str(term) in user:
            filtered_users.append(user)
    messages = get_flashed_messages(with_categories=True)
    print(messages)
    return render_template(
        'users/index.html',
        users=filtered_users,
        user=user,
        search=term,
        messsages=messages,
    )


@app.route('/users/new')
def users_new():
    user = {'nickname': '',
            'email': ''}
    return render_template(
        'users/new.html',
        user=user,
    )

@app.post('/users')
def users_post():
    user = request.form.to_dict()
    with open('data.json', 'w') as file_for_saving:
        json.dumps(user)
    #messages = get_flashed_messages(with_categories=True)
    #print(messages)
    flash('Вы добавлены успешно!', 'success')
    return redirect(url_for('search_users'))


