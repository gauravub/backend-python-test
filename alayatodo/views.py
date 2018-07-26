from alayatodo import app
from flask import (
    g,
    redirect,
    render_template,
    request,
    session,
    )
from alayatodo.models import User, Todo


@app.route('/')
def home():
    with app.open_resource('../README.md', mode='r') as f:
        readme = "".join(l.decode('utf-8') for l in f)
        return render_template('index.html', readme=readme)


@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')
    user = (
        g.db.session.query(User)
        .filter(User.username == username,
                User.password==password)
            .first()
    )

    if user:
        session['user'] = user.get_dict()
        session['logged_in'] = True
        return redirect('/todo')

    return redirect('/login')


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('user', None)
    return redirect('/')


@app.route('/todo/<id>', methods=['GET'])
def todo(id):
    todo_item = (
        g.db.session.query(Todo)
            .filter(Todo.user_id == session['user']['id'],
                    Todo.id == id).one_or_none()
    )
    return render_template('todo.html', todo=todo_item)


#additional rule removed, since 'strict_slashes' is enabled by default, all
# urls that match without trailing slash will trigger a redirect to the same
# URL with the missing slash appended
@app.route('/todo/', methods=['GET'])
def todos_get():
    if not session.get('logged_in'):
        return redirect('/login')
    page = int(request.args.get('page', 1))
    todo_results = (
        g.db.session.query(Todo)
            .filter(Todo.user_id == session['user']['id'])
            .paginate(per_page=3, page=page, error_out=True)
    )
    return render_template('todos.html', pagination=todo_results, todos=todo_results)


@app.route('/todo/', methods=['POST'])
def todos_post():
    if not session.get('logged_in'):
        return redirect('/login')
    user_id = session['user']['id']
    description = request.form.get('description', '')
    new_todo = Todo(user_id=user_id, description=description, complete=0)
    g.db.session.add(new_todo)
    g.db.session.commit()
    return redirect('/todo')


@app.route('/todo/<id>', methods=['POST'])
def todo_delete(id):
    if not session.get('logged_in'):
        return redirect('/login')
    item = Todo.query.filter_by(user_id=session['user']['id'],
                                 id=id).one_or_none()
    if item:
        g.db.session.delete(item)
        g.db.session.commit()
    return redirect('/todo')

@app.route('/todo/<id>/toggle_status', methods=['POST'])
def toggle_status(id):
    if not session.get('logged_in'):
        return redirect('/login')
    item = Todo.query.filter_by(user_id=session['user']['id'],
                                 id=id).one_or_none()
    if item:
        item.complete = (item.complete + 1) % 2
        g.db.session.commit()
    return redirect('/todo')
