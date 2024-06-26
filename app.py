import os
from flask import Flask, jsonify, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource
from flask_cors import CORS
from flask import request
from flask import Flask, make_response, jsonify, request

from models import db, Bird,Products,Workouts

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

# Initialize CORS
CORS(app)

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Birds(Resource):

    def get(self):
        birds = [bird.to_dict() for bird in Bird.query.all()]
        return make_response(jsonify(birds), 200)

api.add_resource(Birds, '/birds')



class AllProducts(Resource):

    def get(self):
        response_body = [product.to_dict() for product in Products.query.all()]
        return make_response(response_body,200)
    def post(self):
        try:
            
            # Ensure required fields are present in the request
            # id = request.json.get('id')
            img = request.json.get('img')
            name = request.json.get('name')
            price = request.json.get('price')
            info = request.json.get('info')

            if not all([img,name,price , info]):
                raise ValueError("Missing required fields")

            new_p = Products(
                
                img=img,
                name=name,
                price=price,
                info=info,
            )
            db.session.add(new_p)
            db.session.commit()

            # Assuming to_dict() method is defined in your Mission model
            rb = new_p.to_dict(rules = ())
            return make_response(rb, 201)

        except ValueError:
            rb = {
                "errors": ["validation errors"]
                }
            return make_response(rb, 400)

api.add_resource(AllProducts, '/products')

class AllWorkouts(Resource):

    def get(self):
        response_body = [workout.to_dict() for workout in Workouts.query.all()]
        return make_response(response_body,200)
    def post(self):
        try:
            
            # Ensure required fields are present in the request
            # id = request.json.get('id')
            img = request.json.get('img')
            name = request.json.get('name')
            timer = request.json.get('timer')
            

            if not all([img,name,timer]):
                raise ValueError("Missing required fields")

            new_w = Workouts(
                
                img=img,
                name=name,
                timer=timer,
                
            )
            db.session.add(new_w)
            db.session.commit()

            # Assuming to_dict() method is defined in your Mission model
            rb = new_w.to_dict(rules = ())
            return make_response(rb, 201)

        except ValueError:
            rb = {
                "errors": ["validation errors"]
                }
            return make_response(rb, 400)

api.add_resource(AllWorkouts, '/workouts')

if __name__ == '__main__':
    app.run()