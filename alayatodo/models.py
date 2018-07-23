from alayatodo import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    todos = db.relationship("Todo", backref="users", order_by="Todo.id")

    def __repr__(self):
        return '<User %r>' % self.username

    def get_dict(self):
        return {'id': self.id, 'username': self.username, 'password': self.password}


class Todo(db.Model):
    __tablename__ = 'todos'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'),
                        nullable=False)
    description = db.Column(db.String(255), nullable=False)
    complete = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<User %r Todo %r>' % self.user_id, self.description

    def get_dict(self):
        return {'id': self.id, 'description': self.description,
                'user_id': self.user_id, 'complete': bool(self.complete)}
