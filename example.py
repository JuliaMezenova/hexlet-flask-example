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
    return render_template('users/start_page.html')

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
    with open("data.json", "r") as f:
        users = json.loads(f.read())
    for user in users:
        if user['nickname'] == id:
            return render_template(
                'users/show.html',
                user=user,
                )        
    if not user:
        return 'Page not found', 404

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
    data = request.form.to_dict()
    errors = validate(data)
    user = data
    if errors:
        return render_template(
            'users/new.html',
            user=data,
            errors=errors,
            ), 422

    with open("data.json", "r") as f:
        users = json.loads(f.read())
    users.append(data)
    with open("data.json", "w") as f:
        f.write(json.dumps(users))
    
    flash(f"{user['nickname']}, Вы добавлены успешно!", 'success')
    return redirect(url_for('search_users'), code=302)


@app.route('/users/<id>/update', methods=['GET', 'POST'])
def user_update(id):
    errors = {}
    with open('data.json') as f:
        users = json.loads(f.read())
    filtered_users = filter(lambda user: user['nickname'] == id, users)
    user=next(filtered_users, None)

    if request.method == 'GET':
        return render_template(
            'users/edit.html',
            user=user,
            errors=errors,
            )
    if request.method == 'POST':
        data = request.form.to_dict()
        errors = validate(data)
        if errors:
            return render_template(
                'users/edit.html',
                user=user,
                errors=errors,
            ), 422
        index_of_user_to_update = users.index(user)
        user.update(data)
        users[index_of_user_to_update] = user
        with open("data.json", "w") as f:
            f.write(json.dumps(users))
        flash('User has been updated', 'success')
        return redirect(url_for('get_user', id=user['nickname']), code=302)


@app.route('/users/<id>/delete', methods=['POST'])
def delete_user(id):
    with open("data.json",'r') as f:
        users = json.loads(f.read())
    filtered_users = filter(lambda user: user['nickname'] == id, users)
    user=next(filtered_users, None)
    users.remove(user)
    with open("data.json","w") as f:
        f.write(json.dumps(users))
    flash('User has been deleted', 'success')
    return redirect(url_for('search_users'))
