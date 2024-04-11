from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 
    #  All authors have a name.
    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError('Name is required.')
        if Author.query.filter(Author.name == name).first():
            raise ValueError('Name must be unique.')
        return name

    #   Author phone numbers are exactly ten digits.
    @validates('phone_number')
    def validate_phone_number(self, key, phone_number):
        if phone_number and len(phone_number) != 10:
            raise ValueError('Author phone number must be exactly ten digits.')
        if phone_number and not phone_number.isdigit():
            raise ValueError('Author phone number must contain only digits.')
        return phone_number


class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    
    # Post title is sufficiently clickbait-y 
    @validates('title')
    def validate_title(self, key, title):
        if not any(keyword in title for keyword in ["Won't Believe", "Secret", "Top", "Guess"]):
            raise ValueError('Post title must contain one of the specified keywords.')
        return title
    
    # Post summary is a maximum of 250 characters. db.String(250)# Post summary is a maximum of 250 characters. db.String(250)
    @validates('content')
    def validate_content(self, key, content):
        if len(content) < 250:
            raise ValueError('Post content must be at least 250 characters long.')
        return content
    
     # Post summary is a maximum of 250 characters. db.String(250)
    @validates('summary')
    def validate_summary(self, key, summary):
        if summary and len(summary) > 250:
            raise ValueError('Post summary cannot exceed 250 characters.')
        return summary
    
    # Post category is either Fiction or Non-Fiction.
    @validates('category')
    def validate_category(self, key, category):
        if category not in ['Fiction', 'Non-Fiction']:
            raise ValueError('Post category must be either "Fiction" or "Non-Fiction".')
        return category
