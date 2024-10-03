from datetime import datetime, timedelta
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///librar.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    role = db.Column(db.String(150), default='user')
    books = db.relationship('Book', backref='user', lazy=True)
    requests = db.relationship('Request', backref='user', lazy=True)
    feedbacks = db.relationship('Feedback', backref='user', lazy=True)
    
    def __repr__(self):
        return f'<User {self.username}>'

class Section(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)
    books = db.relationship('Book', backref='section', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Section {self.name}>'

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    author = db.Column(db.String(150))
    content = db.Column(db.String(255))
    section_id = db.Column(db.Integer, db.ForeignKey('section.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    issue_date = db.Column(db.DateTime, default=datetime.now)
    return_date = db.Column(db.DateTime, default=lambda: datetime.now() + timedelta(weeks=1))
    feedbacks = db.relationship('Feedback', backref='book', lazy=True, cascade='all, delete-orphan')
    
    
    def __repr__(self):
        return f'<Book {self.name}>'

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    content = db.Column(db.String(255), nullable=False)
    
    def __repr__(self):
        return f'<Feedback {self.id} by User {self.user_id} on Book {self.book_id}>'

class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    issue_date = db.Column(db.DateTime, default=datetime.now)
    return_date = db.Column(db.DateTime, default=lambda: datetime.now() + timedelta(weeks=1))
    status = db.Column(db.String(80),  default='pending', nullable=False)
    book = db.relationship('Book', backref='request', lazy=True)
    
    def __repr__(self):
        return f'<Request {self.id} by User {self.user_id} for Book {self.book_id}>'

def init_db():
    with app.app_context():
        db.create_all()
        if User.query.filter_by(username='librarian').first() is None and User.query.filter_by(email='librarian@librar.com').first() is None:
            admin_password = generate_password_hash('librar')
            admin = User(username='librarian', email='librarian@librar.com', password=admin_password, role='admin')
            db.session.add(admin)
            db.session.commit()
            print('Admin user created')
        else:
            print('Admin user already exists')
        
        if Section.query.count() == 0:
            fiction = Section(name='Fiction')
            non_fiction = Section(name='Non-Fiction')
            db.session.add_all([fiction, non_fiction])
            db.session.commit()
            print('Sections created')
        else:
            print('Sections already exist')
            
        if Book.query.count() == 0:
            book1 = Book(name='Book1', author='Author1', content='Content1', section_id=1, issue_date=datetime.now(), return_date=datetime.now() + timedelta(weeks=1))
            book2 = Book(name='Book2', author='Author2', content='Content2', section_id=2, issue_date=datetime.now(), return_date=datetime.now() + timedelta(weeks=1))
            db.session.add_all([book1, book2])
            db.session.commit()
            print('Books created')
        else:
            print('Books already exist')
            
        if Feedback.query.count() == 0:
            db.session.commit()
            print('Feedback table initialized')
        else:
            print('Feedback table already exists')

if __name__ == '__main__':
    init_db()
