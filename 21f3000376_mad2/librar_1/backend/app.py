from flask import Flask, request, jsonify, make_response, send_file
from flask_restful import Api, Resource, reqparse
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from model import db, User, Section, Book, Feedback, Request
from flask_caching import Cache
import redis 
from celery_config import celery
import os

app = Flask(__name__)
redis_client = redis.Redis(host='localhost', port=6379, db=0)
cache = Cache(app, config={'CACHE_TYPE': 'redis', 'CACHE_REDIS': 'redis_client'})
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///librar.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'librar'
celery.conf.update(app.config)



db.init_app(app)
CORS(app, origins='*')
jwt = JWTManager(app)
api = Api(app)


class SignUpResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=True, type=str)
        parser.add_argument('email', required=True, type=str)
        parser.add_argument('password', type=str)
        parser.add_argument('role', type=str, default='user')

        args = parser.parse_args()

        if User.query.filter_by(username=args['username']).first():
            return {"message": 'User already exists'}, 400

        hashed_password = generate_password_hash(args['password'])

        new_user = User(username=args['username'], email=args['email'], password=hashed_password, role=args['role'])

        db.session.add(new_user)
        db.session.commit()

        return {"message": "User created successfully"}, 200


class LoginResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=True, type=str)
        parser.add_argument('password', required=True, type=str)

        args = parser.parse_args()

        user = User.query.filter_by(username=args['username']).first()

        if user and check_password_hash(user.password, args['password']):
            access_token = create_access_token(identity=user.role)
            user_info = {"id": user.id, "username": user.username, "role": user.role}
            return {"access_token": access_token, "user": user_info}, 200
        else:
            return {"message": "Invalid username or password"}, 401


class UserInfo(Resource):
    @cache.cached(timeout=20)
    def get(self):
        users = User.query.filter(User.role != 'admin').all()
        user_info = [{
            "id": user.id,
            "username": user.username,
            "role": user.role
        } for user in users]
        return user_info




class SectionResource(Resource):
    def get(self, section_id=None):
        if section_id:
            section = Section.query.get(section_id)
            if not section:
                return {"message": "Section not found"}, 404
            
            books = Book.query.filter_by(section_id=section_id).all()
            books_data = [{
                "id": book.id,
                "name": book.name,
                "author": book.author,
                "content": book.content,
                "issue_date": book.issue_date.strftime('%Y-%m-%d'),
                "return_date": book.return_date.strftime('%Y-%m-%d')
            } for book in books]
            
            return jsonify({
                "id": section.id,
                "name": section.name,
                "books": books_data
            })
        else:
            sections = Section.query.all()
            sections_data = []
            for section in sections:
                books = Book.query.filter_by(section_id=section.id).all()
                books_data = [{
                    "id": book.id,
                    "name": book.name,
                    "author": book.author,
                    "content": book.content,
                    "issue_date": book.issue_date.strftime('%Y-%m-%d'),
                    "return_date": book.return_date.strftime('%Y-%m-%d')
                } for book in books]
                sections_data.append({
                    "id": section.id,
                    "name": section.name,
                    "books": books_data
                })
            return jsonify(sections_data)

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True, type=str)
        args = parser.parse_args()

        if Section.query.filter_by(name=args['name']).first():
            return {"message": "Section already exists"}, 400
        new_section = Section(name=args['name'])
        db.session.add(new_section)
        db.session.commit()
        return {"message": "Section created successfully"}, 201

    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', required=True, type=int)
        parser.add_argument('name', required=True, type=str)
        args = parser.parse_args()

        section = Section.query.get(args['id'])
        if not section:
            return {"message": "Section not found"}, 404
        section.name = args['name']
        db.session.commit()
        return {"message": "Section updated successfully"}, 200

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', required=True, type=int)
        args = parser.parse_args()

        section = Section.query.get(args['id'])
        if not section:
            return {"message": "Section not found"}, 404

        db.session.delete(section)
        db.session.commit()
        return {"message": "Section deleted successfully"}, 200


class BookResource(Resource):
    def get(self):
        user_id = request.args.get('user_id')
        if user_id:
            books = Book.query.filter_by(user_id=user_id).all()
        else:
            books = Book.query.all()
        return jsonify([{
            "id": book.id,
            "name": book.name,
            "author": book.author,
            "content": book.content,
            "section_id": book.section_id,
            "user_id": book.user_id,
            "created_at": book.created_at,
            "issue_date": book.issue_date.strftime('%Y-%m-%d'),
            "return_date": book.return_date.strftime('%Y-%m-%d')
        } for book in books])

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True, type=str)
        parser.add_argument('author', required=False, type=str)
        parser.add_argument('content', required=False, type=str)
        parser.add_argument('section_id', required=True, type=int)
        parser.add_argument('user_id', required=True, type=int)
        parser.add_argument('issue_date', required=False, type=str)
        parser.add_argument('return_date', required=False, type=str)
        args = parser.parse_args()

        issue_date = datetime.strptime(args['issue_date'], '%Y-%m-%d') if args['issue_date'] else datetime.now()
        return_date = datetime.strptime(args['return_date'], '%Y-%m-%d') if args['return_date'] else issue_date + timedelta(weeks=1)

        new_book = Book(
            name=args['name'],
            author=args.get('author'),
            content=args.get('content'),
            section_id=args['section_id'],
            user_id=args['user_id'],
            issue_date=issue_date,
            return_date=return_date
        )
        db.session.add(new_book)
        db.session.commit()
        return {"message": "Book added successfully"}, 201

    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', required=True, type=int)
        parser.add_argument('name', required=False, type=str)
        parser.add_argument('author', required=False, type=str)
        parser.add_argument('content', required=False, type=str)
        parser.add_argument('section_id', required=False, type=int)
        parser.add_argument('user_id', required=False, type=int)
        parser.add_argument('issue_date', required=False, type=str)
        parser.add_argument('return_date', required=False, type=str)
        args = parser.parse_args()

        book = Book.query.get(args['id'])
        if not book:
            return {"message": "Book not found"}, 404

        if args['name']:
            book.name = args['name']
        if args['author']:
            book.author = args['author']
        if args['content']:
            book.content = args['content']
        if args['section_id']:
            book.section_id = args['section_id']
        if args['user_id']:
            book.user_id = args['user_id']
        if args['issue_date']:
            book.issue_date = datetime.strptime(args['issue_date'], '%Y-%m-%d')
        if args['return_date']:
            book.return_date = datetime.strptime(args['return_date'], '%Y-%m-%d')

        db.session.commit()
        return {"message": "Book updated successfully"}, 200

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', required=True, type=int)
        args = parser.parse_args()

        book = Book.query.get(args['id'])
        if not book:
            return {"message": "Book not found"}, 404

        db.session.delete(book)
        db.session.commit()
        return {"message": "Book deleted successfully"}, 200


class RequestResource(Resource):
    def get(self, user_id):
        if user_id != 1:
            requests = Request.query.filter_by(user_id=user_id).all()
        else:
            requests = Request.query.all()

        return jsonify([{
            "id": request.id,
            "user_id": request.user_id,
            "book_id": request.book_id,
            "book_name": request.book.name,
            "book_author": request.book.author,
            "issue_date": request.issue_date.strftime('%Y-%m-%d'),
            "return_date": request.return_date.strftime('%Y-%m-%d'),
            "status": request.status,
            "book": {
                "content": request.book.content if request.book else "No content available",
                "section_id": request.book.section_id,
                "section_name": request.book.section.name
            },
            "user": {
                "username": request.user.username,
                "email": request.user.email
            }
        } for request in requests])

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', required=True, type=int)
        parser.add_argument('book_id', required=True, type=int)
        args = parser.parse_args()

        # Check if the user has 5 or more books accepted or pending
        active_requests_count = Request.query.filter_by(user_id=args['user_id']).filter(Request.status.in_(['pending', 'accepted'])).count()
        if active_requests_count >= 5:
            return {"message": "You cannot request more than 5 books at a time. Please return some books first."}, 400

        # Check if the user has a pending or accepted request for the same book
        existing_request = Request.query.filter_by(user_id=args['user_id'], book_id=args['book_id']).filter(Request.status.in_(['pending', 'accepted'])).first()
        if existing_request:
            return {"message": "You have already requested this book or the request is still pending."}, 400

        # Set issue_date to today and return_date to one week from today
        issue_date = datetime.now()
        return_date = issue_date + timedelta(weeks=1)

        new_request = Request(
            user_id=args['user_id'],
            book_id=args['book_id'],
            status='pending',
            issue_date=issue_date,
            return_date=return_date
        )
        db.session.add(new_request)
        db.session.commit()
        return {"message": "Request created successfully"}, 201

    def put(self, request_id):
        parser = reqparse.RequestParser()
        parser.add_argument('status', required=True, type=str)
        args = parser.parse_args()

        request = Request.query.get(request_id)
        if not request:
            return {"message": "Request not found"}, 404

        request.status = args['status']

        if args['status'] == 'accepted':
            book = Book.query.get(request.book_id)
            book.user_id = request.user_id
        elif args['status'] == 'revoked':
            book = Book.query.get(request.book_id)
            book.user_id = None

        db.session.commit()
        return {"message": "Request updated successfully"}, 200

    def delete(self, request_id):
        request = Request.query.get(request_id)
        if not request:
            return {"message": "Request not found"}, 404

        db.session.delete(request)
        db.session.commit()
        return {"message": "Request deleted successfully"}, 200
    
    

class ReturnBookResource(Resource):
    def put(self, book_id):
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', required=True, type=int)
        args = parser.parse_args()

        request = Request.query.filter_by(book_id=book_id, user_id=args['user_id'], status='accepted').first()
        if not request:
            return {"message": "Request not found"}, 404

        request.status = 'returned'
        book = Book.query.get(book_id)
        book.user_id = None

        db.session.commit()
        return {"message": "Book returned successfully"}, 200


class FeedbackResource(Resource):
    def get(self, book_id=None):
        if book_id:
            feedbacks = Feedback.query.filter_by(book_id=book_id).all()
            if not feedbacks:
                return jsonify([])

            return jsonify([{
                "id": feedback.id,
                "user_id": feedback.user_id,
                "book_id": feedback.book_id,
                "content": feedback.content,
                "user": {"username": feedback.user.username}  
            } for feedback in feedbacks])
        else:
            feedbacks = Feedback.query.all()
            return jsonify([{
                "id": feedback.id,
                "user_id": feedback.user_id,
                "book_id": feedback.book_id,
                "content": feedback.content,
                "user": {"username": feedback.user.username}  
            } for feedback in feedbacks])

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', required=True, type=int)
        parser.add_argument('book_id', required=True, type=int)
        parser.add_argument('content', required=True, type=str)
        args = parser.parse_args()

        new_feedback = Feedback(user_id=args['user_id'], book_id=args['book_id'], content=args['content'])
        db.session.add(new_feedback)
        db.session.commit()
        return {"message": "Feedback added successfully"}, 201



class BooksInLibraryStatsResource(Resource):
    @cache.cached(timeout=20)
    def get(self):
        sections = Section.query.all()
        books_in_library = {}

        for section in sections:
            section_name = section.name
            books_in_library[section_name] = Book.query.filter_by(section_id=section.id).count()

        return {
            "sections": list(books_in_library.keys()),
            "counts": list(books_in_library.values())
        }

class BooksIssuedStatsResource(Resource):
    @cache.cached(timeout=20)
    def get(self):
        sections = Section.query.all()
        books_issued = {}

        for section in sections:
            section_name = section.name
            books_issued[section_name] = Book.query.filter(Book.section_id == section.id, Book.user_id.isnot(None)).count()

        return {
            "sections": list(books_issued.keys()),
            "counts": list(books_issued.values())
        }

class LibraryStatsResource(Resource):
    def get(self):
        total_books = Book.query.count()
        total_sections = Section.query.count()
        total_books_issued = Request.query.filter_by(status='accepted').count()
        total_users = User.query.filter(User.role != 'admin').count()

        return {
            "total_books": total_books,
            "total_sections": total_sections,
            "total_books_issued": total_books_issued,
            "total_users": total_users
        }




class ExportResource(Resource):
    @jwt_required()
    def post(self,user_id):
        user_role = get_jwt_identity()
        if user_role !='admin':
            return jsonify({'message':'access deneid'})
        try:
            from tasks import export_sections_details_as_csv

            csv_data = export_sections_details_as_csv(user_id)

            response = make_response(csv_data)

            response.headers['Content-Disposition'] = 'attachment;filename=section_report.csv'

            response.headers['Content-type'] = 'text/csv'

            return response
        except Exception as e:
            return jsonify(e),500


class SingleBookResource(Resource):
    def get(self, book_id):
        book = Book.query.get(book_id)
        if not book:
            return {"message": "Book not found"}, 404
        return jsonify({
            "id": book.id,
            "name": book.name,
            "author": book.author,
            "content": book.content,
            "section_id": book.section_id,
            "user_id": book.user_id,
            "created_at": book.created_at,
            "issue_date": book.issue_date.strftime('%Y-%m-%d'),
            "return_date": book.return_date.strftime('%Y-%m-%d')
        })






api.add_resource(LibraryStatsResource, '/api/stats/library')
api.add_resource(SingleBookResource, '/api/book/<int:book_id>')
api.add_resource(ExportResource,'/exportcsv/<int:user_id>')
api.add_resource(BooksInLibraryStatsResource, '/api/stats/books-in-library')
api.add_resource(BooksIssuedStatsResource, '/api/stats/books-issued')
api.add_resource(FeedbackResource, '/api/feedback', '/api/feedback/<int:book_id>')
api.add_resource(ReturnBookResource, '/api/request/return/<int:book_id>')
api.add_resource(RequestResource, '/api/request', '/api/request/<int:request_id>', '/api/request/user/<int:user_id>')
api.add_resource(BookResource, '/api/book')
api.add_resource(SectionResource, '/api/section', '/api/section/<int:section_id>')
api.add_resource(UserInfo, '/api/userinfo')
api.add_resource(SignUpResource, '/api/signup')
api.add_resource(LoginResource, '/api/login')


if __name__ == '__main__':
    app.run(debug=True)
