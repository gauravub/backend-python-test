from alayatodo import app
from flask import (
    g,
    redirect,
    render_template,
    request,
    session,
    jsonify,
    flash
    )
from alayatodo.models import User, Todo
from decorators import login_required


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
        flash('Welcome {}'.format(user.username))
        return redirect('/todo')
    else:
        flash('Incorrect login credentials. Kindly try again.')
        return redirect('/login')


@app.route('/logout')
def logout():
    flash('You were logged out.')
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

@app.route('/todo/<id>/json', methods=['GET'])
@login_required
def get_json(id):
    todo_item = (
        g.db.session.query(Todo)
            .filter(Todo.user_id == session['user']['id'],
                    Todo.id == id).one_or_none()
    )
    return jsonify(todo_item.get_dict())


#additional rule removed, since 'strict_slashes' is enabled by default, all
# urls that match without trailing slash will trigger a redirect to the same
# URL with the missing slash appended
@app.route('/todo/', methods=['GET'])
@login_required
def todos_get():
    page = int(request.args.get('page', 1))
    todo_results = (
        g.db.session.query(Todo)
            .filter(Todo.user_id == session['user']['id'])
            .paginate(per_page=3, page=page, error_out=True)
    )
    return render_template('todos.html', pagination=todo_results, todos=todo_results)


@app.route('/todo/', methods=['POST'])
@login_required
def todos_post():
    user_id = session['user']['id']
    description = request.form.get('description')
    new_todo = Todo(user_id=user_id, description=description, complete=0)
    g.db.session.add(new_todo)
    g.db.session.commit()
    flash('New Todo item was added with id {}.'.format(new_todo.id))
    return redirect('/todo')


@app.route('/todo/<int:id>', methods=['POST'])
@login_required
def todo_delete(id):

    item = Todo.query.filter_by(user_id=session['user']['id'],
                                 id=id).one_or_none()
    if item:
        flash('Todo item with id {} deleted.'.format(item.id))
        g.db.session.delete(item)
        g.db.session.commit()
    return redirect('/todo')

@app.route('/todo/<id>/toggle_status', methods=['POST'])
def toggle_status(id):
    item = Todo.query.filter_by(user_id=session['user']['id'],
                                 id=id).one_or_none()
    if item:
        item.complete = (item.complete + 1) % 2
        g.db.session.commit()
    return redirect('/todo')
