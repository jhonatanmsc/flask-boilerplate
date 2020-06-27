from datetime import datetime

from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

user_groups = db.Table('user_groups',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('group_id', db.Integer, db.ForeignKey('groups.id'), primary_key=True)
)

user_permissions = db.Table('user_permissions',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('permission_id', db.Integer, db.ForeignKey('permissions.id'), primary_key=True)
)

group_permissions = db.Table('group_permissions',
    db.Column('group_id', db.Integer, db.ForeignKey('groups.id'), primary_key=True),
    db.Column('permission_id', db.Integer, db.ForeignKey('permissions.id'), primary_key=True)
)


class ContentType(db.Model):
    __tablename__ = 'content_type'
    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(100))
    logs = db.relationship('Log', backref='content_type', lazy=True)

    def __init__(self, model):
        self.model = model

    def __repr__(self):
        return f'<ContentType: {self.model}>'


class Permission(db.Model):
    __tablename__ = 'permissions'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    codename = db.Column(db.String(100), unique=True)
    content_type_id = db.Column(db.Integer, db.ForeignKey('content_type.id'), nullable=False)

    def __init__(self, name, codename):
        self.name = name
        self.codename = codename

    def __repr__(self):
        return f'<Permission: {self.codename}>'


class Group(db.Model):
    __tablename__ = 'groups'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    group_permissions = db.relationship('Permission', secondary=group_permissions, lazy='subquery',
                                        backref=db.backref('groups', lazy=True))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'<Group: {self.name}>'


@login_manager.user_loader
def get_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80))
    name = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True, nullable=False)
    last_login = db.Column(db.DateTime)
    is_superuser = db.Column(db.Boolean, default=False)
    date_joined = db.Column(db.DateTime, default=datetime.utcnow)
    is_staff = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    user_groups = db.relationship('Group', secondary=user_groups, lazy='subquery',
                                  backref=db.backref('users', lazy=True))
    user_permissions = db.relationship('Permission', secondary=user_permissions, lazy='subquery',
                                       backref=db.backref('users', lazy=True))
    logs = db.relationship('Log', backref='user', lazy=True)

    def __init__(self, username, password, name, email, last_login, is_superuser, date_joined, is_staff, is_active):
        self.username = username
        self.password = generate_password_hash(password)
        self.name = name
        self.email = email
        self.last_login = last_login
        self.is_superuser = is_superuser
        self.date_joined = date_joined
        self.is_staff = is_staff
        self.is_active = is_active

    def __repr__(self):
        return f'<User: {self.username}>'

    def verify_password(self, pwd):
        return check_password_hash(self.password, pwd)


class Log(db.Model):
    __tablename__ = 'logs'
    id = db.Column(db.Integer, primary_key=True)
    action_time = db.Column(db.DateTime())
    object_id = db.Column(db.Integer)
    object_repr = db.Column(db.String(254))
    change_msg = db.Column(db.String(254))
    action_flag = db.Column(db.Integer)
    content_type_id = db.Column(db.Integer, db.ForeignKey('content_type.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __init__(self, action_time, object_id, object_repr, change_msg, action_flag, content_type_id, user_id):
        self.action_time = action_time
        self.object_id = object_id
        self.object_repr = object_repr
        self.change_msg = change_msg
        self.action_flag = action_flag
        self.content_type_id = content_type_id
        self.user_id = user_id

    def __repr__(self):
        return f'<Log: >'
