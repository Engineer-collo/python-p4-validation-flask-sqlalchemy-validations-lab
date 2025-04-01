from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 
    @validates('name')
    def validate_name(self, key, value):
        """Ensure name is present and unique."""
        if not value.strip():
            raise ValueError("Author name cannot be empty.")
        
        existing_author = Author.query.filter_by(name=value).first()
        if existing_author:
            raise ValueError("An author with this name already exists.")
        
        return value 
      
    @validates('phone_number')
    def validate_phone_number(self, key, value):
        """Ensure phone number is a valid phone number."""
        if not value.strip():
            return None
        
        if not value.isdigit():
            raise ValueError("Phone number must be a number.")
        
        if len(value) != 10:
            raise ValueError("Phone number must have 10 digits.")
        
        return value

    
        



    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String(250))
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators  
    @validates('title')
    def validate_title(self, key, value):
        """Ensure title is present."""
        if not value.strip():
            raise ValueError("Post title cannot be empty.")
        
        return value
     
    @validates('content')
    def validate_content(self, key, value):
        """Ensure content is present."""
        if not value.strip():
            raise ValueError("Post content cannot be empty.")
        if len(value) < 250:
            raise ValueError("Post content cannot be less than 250.")
        return value
    

    @validates('summary')
    def validate_summary(self, key, value):
        """Ensure summary is present."""
        if not value.strip():
            raise ValueError("Post summary cannot be empty.")
        if len(value) > 250:
            raise ValueError("Post summary cannot be more than 250.")
        return value
    
    @validates('category')
    def validate_category(self, key, value):
        """Ensure category is present."""
        category = ['Fiction', 'Non-Fiction']  
        for n in category:
            if value not in category:
                raise ValueError("Post category must be either Fiction or Non-Fiction.")
        
        return value
    
    @validates('title')
    def validate_title(self, key, value):
        """Ensure the title is clickbait-y."""
        clickbait_phrases = ["Won't Believe", "Secret", "Top", "Guess"]
        if not any(phrase in value for phrase in clickbait_phrases):
            raise ValueError("Title must contain one of the following: 'Won't Believe', 'Secret', 'Top', 'Guess'.")
        return value


    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
