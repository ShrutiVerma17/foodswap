from app import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    uni = db.Column(db.String(), unique=True)
    points = db.Column(db.Integer())
    # created_posts = db.relationship('Post', backref='users', lazy=True)

    def __init__(self, name, uni):
        self.name = name
        self.uni = uni
        self.points = 1 

    def __repr__(self):
        return '<id {}>'.format(self.id)
    
    def serialize(self):
        return {
            'id': self.id, 
            'name': self.name,
            'uni': self.uni,
            'points': self.points
        }

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(150))
    dietary_info = db.Column(db.String(150))
    img_url = db.Column(db.String())
    creating_user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    reserving_user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    creator = db.relationship("User", foreign_keys=[creating_user_id])
    buyer = db.relationship("User", foreign_keys=[reserving_user_id])

    def __init__(self, author, description, dietary_info, img_url):
        self.creating_user_id = author
        self.description = description
        self.dietary_info = dietary_info
        self.img_url = img_url

    def __repr__(self):
        return '<id {}>'.format(self.id)
    
    def serialize(self):
        return {
            'id': self.id, 
            'author': self.creating_user_id,
            'description': self.description,
            'dietary_info': self.dietary_info,
            'img_url': self.img_url,
            'reserver': self.reserving_user_id
        }