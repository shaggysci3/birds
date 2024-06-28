from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin


from config import db, bcrypt, metadata
from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property



# db = SQLAlchemy()
# Association table to store many-to-many relationship between employees and meetings
user_workouts = db.Table(
    'user_workouts',
    metadata,
    db.Column('user_id', db.Integer, db.ForeignKey(
        'users.id'), primary_key=True),
    db.Column('workout_id', db.Integer, db.ForeignKey(
        'workouts.id'), primary_key=True)
)

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    _password_hash = db.Column(db.String)
    name = db.Column(db.String)

    
    # Relationship mapping the users to related workouts
    workouts = db.relationship(
        'Workouts', secondary=user_workouts, back_populates='users')
    # Setialization rules for users
    serialize_rules = ('-workouts.users',)
   
    
    @hybrid_property
    def password_hash(self):
      raise Exception('Password hashes may not be viewed')
    @password_hash.setter
    def password_hash(self, password):
      password_hash = bcrypt.generate_password_hash(password.encode('utf-8'))
      self._password_hash = password_hash.decode('utf-8')
    def authenticate(self, password):
      return bcrypt.check_password_hash(
      self._password_hash, password.encode('utf-8')
      )
    def __repr__(self):
        return f'<User {self.id}: {self.name}>'
    
    @validates('name')
    def validate_name(self,attr,value):
        if value:
            return value
        else:
            raise ValueError('please enter a name')
    

class Bird(db.Model, SerializerMixin):
    __tablename__ = 'birds'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    species = db.Column(db.String)

    def __repr__(self):
        return f'<Bird {self.name} | Species: {self.species}>'
    
class Products(db.Model, SerializerMixin):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    img = db.Column(db.String)
    name = db.Column(db.String)
    price = db.Column(db.Integer)
    info = db.Column(db.String)

    def __repr__(self):
        return f'<Products {self.name} | {self.id}>'
    


class Workouts(db.Model, SerializerMixin):
    __tablename__ = 'workouts'

    id = db.Column(db.Integer, primary_key=True)
    img = db.Column(db.String)
    name = db.Column(db.String)
    timer = db.Column(db.Integer)

    # Relationship mapping the workouts to related users
    users = db.relationship(
        'User', secondary=user_workouts, back_populates='workouts')
     # Setialization rules for users
    serialize_rules = ('-users.workouts',)

    def __repr__(self):
        return f'<Workouts {self.name} | {self.id}>'
    