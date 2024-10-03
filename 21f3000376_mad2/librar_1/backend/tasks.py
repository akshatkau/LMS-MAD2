import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from io import StringIO
from datetime import datetime, timedelta
from celery_config import celery
from app import app
from model import db, User, Section, Book, Request
import csv

@celery.task
def generate_monthly_report():
    with app.app_context():
        current_month = datetime.now().strftime('%B')
        current_year = datetime.now().year
        start_of_month = datetime.now().replace(day=1)

        users = User.query.filter(User.role != 'librarian').all()
        for user in users:
            requests_accepted = Request.query.filter(Request.user_id == user.id, Request.issue_date >= start_of_month, Request.status == 'accepted').all()
            books_list = ""
            if requests_accepted:
                for request in requests_accepted:
                    book = Book.query.filter_by(id=request.book_id).first()
                    if book:
                        books_list += f"<li>{book.name} by {book.author}, Issued on: {request.issue_date.strftime('%Y-%m-%d')}, Return Date: {request.return_date.strftime('%Y-%m-%d')}</li>"
            else:
                books_list = "<li>No books issued this month.</li>"
            
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Monthly Activity Report</title>
            </head>
            <body>
                <p>Dear {user.username},</p>
                <p>Here is your monthly activity report for {current_month}, {current_year}:</p>
                <ul>
                    {books_list}
                </ul>
            </body>
            </html>"""
            print(f"Sending Monthly Activity Report to {user.email}")
            send_email(user.email, html_content, "Monthly Activity Report")

@celery.task
def daily_reminders():
    with app.app_context():
        today = datetime.now().date()
        print(Request.query.filter(Request.return_date <= today + timedelta(days=8)).all())
        print("Daily Reminders Task")
        
        for request in Request.query.filter(Request.return_date <= today + timedelta(days=8)).all():
            user = request.user
            print(request.status)
            
            if request.status == 'accepted':
                reminder_content = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <title>Book Return Reminder</title>
                </head>
                <body>
                    <h3>Dear {user.username},</h3>
                    <p>This is a reminder to return the book titled '{request.book.name}' which is due for return on {request.return_date.strftime('%Y-%m-%d')}.</p>
                    <p>Please visit the library app to return the book.</p>
                </body>
                </html>
                """
                send_email(user.email, reminder_content, "Book Return Reminder")

def send_email(to_email, html_content, subject):
    from_email = 'librar@gmail.com'
    msg = MIMEMultipart('alternative')
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    part1 = MIMEText(html_content, 'html')
    msg.attach(part1)

    smtp_server = 'localhost'
    smtp_port = 1025

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        print(f"Email sent to {to_email} with subject: {subject}")
        server.sendmail(from_email, to_email, msg.as_string())

@celery.task
def export_sections_details_as_csv(created_user_id):
    sections = Section.query.all()

    csv_buffer = StringIO()
    csv_writer = csv.writer(csv_buffer)
    
    csv_writer.writerow(['Section Name', 'Book Name', 'Author', 'Create Date'])

    for section in sections:
        books = Book.query.filter_by(section_id=section.id).all()
        for book in books:
            csv_writer.writerow([
                section.name,
                book.name,
                book.author,
                book.issue_date.strftime('%Y-%m-%d') if book.issue_date else '',
            ])

    base_dir = os.path.abspath(os.path.dirname(__name__))
    csv_file_path = os.path.join(base_dir, 'csv/section_report.csv')
    with open(csv_file_path, 'w') as csv_file:
        csv_file.write(csv_buffer.getvalue())

    return csv_buffer.getvalue()
