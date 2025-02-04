import os
from flask import Flask, jsonify, make_response
from flask_mail import Mail, Message
from flask_migrate import Migrate
from flask_restful import Api, Resource
from flask_cors import CORS
from flask import request
from flask import Flask, make_response, jsonify, request

from models import Bird,Products,Workouts,User,Show,user_workouts,Ratings,About,VideoID,Songs,FeaturedAlbum

from config import app,db,mail


# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.json.compact = False

# Initialize CORS
CORS(app)

# migrate = Migrate(app, db)
# db.init_app(app)

api = Api(app)

class Login(Resource):
  def post(self):
    data = request.get_json()
    username = data['username']
    password = data['password']
    user = User.query.filter(User.username == username).first()
    if user:
      if user.authenticate(password):
          return make_response(user.to_dict(rules=()), 200)
      return {'error': "Unauthorized"}, 401
    return {'error': "User Not Found"}, 404 
  
api.add_resource(Login,'/login')

# sending an email with flask test 1
# class SendEmail(Resource):
#     def post(self):
#         try:
#             # Parse request data
#             data = request.get_json()
#             recipient = data.get('recipient')  # Email address of the recipient
#             subject = data.get('subject', 'No Subject')  # Default subject
#             message_body = data.get('message', 'No message content')  # Default message

#             if not recipient:
#                 return {"error": "Recipient email is required"}, 400

#             # Create email message
#             msg = Message(
#                 subject=subject,
#                 recipients=[recipient],  # List of recipients
#                 body=message_body
#             )
#             mail.send(msg)  # Send the email

#             return {"message": "Email sent successfully"}, 200
#         except Exception as e:
#             return {"error": str(e)}, 500
# api.add_resource(SendEmail, '/send-email')

class AllUsers(Resource):
    
    def get(self):
        users = User.query.all()
        # for user in users:
        #     print(user.__dict__)  # Print user attributes to debug
        response_body = [user.to_dict(rules=('-workouts.users', '-user_workouts')) for user in users]
        return make_response(jsonify(response_body), 200)
    
    def post(self):
        try:
            # Ensure required fields are present in the request
            name = request.json.get('name')
            password = request.json.get('password')
            username = request.json.get('username')

            if not all([name, username, password]):
                raise ValueError("Missing required fields")

            new_u = User(
                name=name,
                username=username,
            )
            new_u.password_hash = password
            db.session.add(new_u)
            db.session.commit()

            # Assuming to_dict() method is defined in your Mission model
            rb = new_u.to_dict(rules = ('-workouts', '-user_workouts'))
            return make_response(rb, 201)

        except ValueError:
            rb = {
                "errors": ["validation errors"]
                }
            return make_response(rb, 400)

api.add_resource(AllUsers,'/users')

class UserById(Resource):
    def get(self,id):

        user = User.query.filter(User.id == id).first()

        if user:
            response_body = user.to_dict(rules = ())
            return make_response(response_body,200)
        else:
            response_body = {
                "error": "User not found"
            }
            return make_response(response_body,404)
    
    def delete(self, id ):
        user = User.query.filter(User.id == id).first()

        if user:
            db.session.delete(user)
            db.session.commit()
            response_body = {}
            return make_response(response_body, 204)
        else:
            response_body = {
                "error": "User not found"
            }
            return make_response(response_body,404)
    
    def patch(self, id):
        user = User.query.filter(User.id == id).first()

        if user:
            try:
                # Get the data from the PATCH request
                data = request.json

                # Update user attributes if present in the request
                if 'name' in data:
                    user.name = data['name']
                if 'password' in data:
                    user.password = data['password']
                if 'username' in data:
                    user.username = data['username']

                # Commit changes to the database
                db.session.commit()

                # Return the updated user
                response_body = user.to_dict(rules=())
                return make_response(response_body, 200)

            except ValueError:
                response_body = {
                    "error": "Invalid data in the request"
                }
                return make_response(response_body, 400)
        else:
            response_body = {
                "error": "User not found"
            }
            return make_response(response_body, 404)

api.add_resource(UserById,'/users/<int:id>')



class Birds(Resource):

    def get(self):
        birds = [bird.to_dict() for bird in Bird.query.all()]
        return make_response(jsonify(birds), 200)

api.add_resource(Birds, '/birds')



class AllShows(Resource):

    def get(self):
        response_body = [show.to_dict() for show in Show.query.all()]
        return make_response(response_body,200)
    def post(self):
        try:
            
            # Ensure required fields are present in the request
            # id = request.json.get('id')
            img = request.json.get('img')
            name = request.json.get('name')
            date = request.json.get('date')
            time = request.json.get('time')
            location = request.json.get('location')

            if not all([img ,name,date , time, location]):
                raise ValueError("Missing required fields")

            new_s = Show(
                
                img=img,
                name=name,
                date=date,
                time=time,
                location=location,
            )
            db.session.add(new_s)
            db.session.commit()

            # Assuming to_dict() method is defined in your Mission model
            rb = new_s.to_dict(rules = ())
            return make_response(rb, 201)

        except ValueError:
            rb = {
                "errors": ["validation errors"]
                }
            return make_response(rb, 400)

api.add_resource(AllShows, '/shows')

class ShowById(Resource):
    def get(self,id):

        show = Show.query.filter(Show.id == id).first()

        if show:
            response_body = show.to_dict(rules = ())
            return make_response(response_body,200)
        else:
            response_body = {
                "error": "User not found"
            }
            return make_response(response_body,404)
    
    def delete(self, id ):
        show = Show.query.filter(Show.id == id).first()

        if show:
            db.session.delete(show)
            db.session.commit()
            response_body = {}
            return make_response(response_body, 204)
        else:
            response_body = {
                "error": "User not found"
            }
            return make_response(response_body,404)
    
    def patch(self, id):
        show = Show.query.filter(Show.id == id).first()

        if show:
            try:
                # Get the data from the PATCH request
                data = request.json

                # Update user attributes if present in the request
                if 'username' in data:
                    show.img = data['img']
                if 'name' in data:
                    show.name = data['name']
                if ' ' in data:
                    show.date = data['date']
                if 'username' in data:
                    show.time = data['time']
                if 'username' in data:
                    show.location = data['location']

                # Commit changes to the database
                db.session.commit()

                # Return the updated user
                response_body = show.to_dict(rules=())
                return make_response(response_body, 200)

            except ValueError:
                response_body = {
                    "error": "Invalid data in the request"
                }
                return make_response(response_body, 400)
        else:
            response_body = {
                "error": "User not found"
            }
            return make_response(response_body, 404)

api.add_resource(ShowById,'/shows/<int:id>')

class Song(Resource):

    def get(self):
        response_body = [song.to_dict() for song in Songs.query.all()]
        return make_response(response_body,200)
    def post(self):
        try:
            
            # Ensure required fields are present in the request
            # id = request.json.get('id')
            
            song = request.json.get('song')
            album_id = request.json.get('album_id')
            

            if not all([song,album_id]):
                raise ValueError("Missing required fields")

            new_s = Songs(
                
                song =song,
                album_id=album_id
            )
            db.session.add(new_s)
            db.session.commit()

            # Assuming to_dict() method is defined in your Mission model
            rb = new_s.to_dict(rules = ())
            return make_response(rb, 201)

        except ValueError:
            rb = {
                "errors": ["validation errors"]
                }
            return make_response(rb, 400)

api.add_resource(Song, '/song')

class SongById(Resource):
    def get(self,id):

        song = Songs.query.filter(Songs.id == id).first()

        if song:
            response_body = song.to_dict(rules = ())
            return make_response(response_body,200)
        else:
            response_body = {
                "error": "Song not found"
            }
            return make_response(response_body,404)
    
    # def delete(self, id ):
    #     show = Show.query.filter(Show.id == id).first()

    #     if show:
    #         db.session.delete(show)
    #         db.session.commit()
    #         response_body = {}
    #         return make_response(response_body, 204)
    #     else:
    #         response_body = {
    #             "error": "User not found"
    #         }
    #         return make_response(response_body,404)
    
    def patch(self, id):
        song = Songs.query.filter(Songs.id == id).first()

        if song:
            try:
                # Get the data from the PATCH request
                data = request.json

                # Update user attributes if present in the request
                if 'song' in data:
                    song.song = data['song']
                if 'album_id' in data:
                    song.album_id = data['album_id']
                

                # Commit changes to the database
                db.session.commit()

                # Return the updated user
                response_body = song.to_dict(rules=())
                return make_response(response_body, 200)

            except ValueError:
                response_body = {
                    "error": "Invalid data in the request"
                }
                return make_response(response_body, 400)
        else:
            response_body = {
                "error": "User not found"
            }
            return make_response(response_body, 404)

api.add_resource(SongById,'/song/<int:id>')

class Album(Resource):

    def get(self):
        response_body = [album.to_dict() for album in FeaturedAlbum.query.all()]
        return make_response(response_body,200)
    def post(self):
        try:
            
            # Ensure required fields are present in the request
            # id = request.json.get('id')
            
            img = request.json.get('img')
            
            

            if not all([img]):
                raise ValueError("Missing required fields")

            new_a = FeaturedAlbum(
                img=img
            )
            db.session.add(new_a)
            db.session.commit()

            # Assuming to_dict() method is defined in your Mission model
            rb = new_a.to_dict(rules = ())
            return make_response(rb, 201)

        except ValueError:
            rb = {
                "errors": ["validation errors"]
                }
            return make_response(rb, 400)

api.add_resource(Album, '/album')

class AlbumById(Resource):
    def get(self,id):

        albums = FeaturedAlbum.query.filter(FeaturedAlbum.id == id).first()

        if albums:
            response_body = albums.to_dict(rules = ())
            return make_response(response_body,200)
        else:
            response_body = {
                "error": "Album not found"
            }
            return make_response(response_body,404)
    
    # def delete(self, id ):
    #     show = Show.query.filter(Show.id == id).first()

    #     if show:
    #         db.session.delete(show)
    #         db.session.commit()
    #         response_body = {}
    #         return make_response(response_body, 204)
    #     else:
    #         response_body = {
    #             "error": "User not found"
    #         }
    #         return make_response(response_body,404)
    
    # def patch(self, id):
    #     song = Songs.query.filter(Songs.id == id).first()

    #     if song:
    #         try:
    #             # Get the data from the PATCH request
    #             data = request.json

    #             # Update user attributes if present in the request
    #             if 'song' in data:
    #                 song.song = data['song']
    #             if 'album_id' in data:
    #                 song.album_id = data['album_id']
                

    #             # Commit changes to the database
    #             db.session.commit()

    #             # Return the updated user
    #             response_body = song.to_dict(rules=())
    #             return make_response(response_body, 200)

    #         except ValueError:
    #             response_body = {
    #                 "error": "Invalid data in the request"
    #             }
    #             return make_response(response_body, 400)
    #     else:
    #         response_body = {
    #             "error": "User not found"
    #         }
    #         return make_response(response_body, 404)

api.add_resource(AlbumById,'/album/<int:id>')


class AllWorkouts(Resource):

    def get(self):
        workouts = Workouts.query.all()

        response_body = [workout.to_dict(rules=('-users.workouts', '-user_workouts')) for workout in workouts]
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

class WorkoutById(Resource):
    def get(self,id):
        
        workout = Workouts.query.filter(Workouts.id == id).first()

        if workout:
            response_body = workout.to_dict(rules = ())
            return make_response(response_body,200)
        else:
            response_body = {
                "error": "User not found"
            }
            return make_response(response_body,404)
    
    def delete(self, id ):
        workout = Workouts.query.filter(Workouts.id == id).first()

        if workout:
            db.session.delete(workout)
            db.session.commit()
            response_body = {}
            return make_response(response_body, 204)
        else:
            response_body = {
                "error": "User not found"
            }
            return make_response(response_body,404)
    
    

api.add_resource(WorkoutById,'/workouts/<int:id>')


class UserWorkout(Resource):
    def get(self,u_id,w_id):
        
        response_body = [uw.to_dict(rules=()) for uw in user_workouts.query.all()]
        return make_response(response_body,200)
    
    def post(self,u_id,w_id):
        try:
            userId = request.json.get('userId')
            workoutId = request.json.get('workoutId')

            user = User.query.filter(User.id == userId).first()
            workout = Workouts.query.filter(Workouts.id == workoutId).first()
            

            if not all([user, workout]):
                raise ValueError("Missing required fields")

            
            
            user.workouts.append(workout)
            db.session.commit()

            # Assuming to_dict() method is defined in your Mission model
            workouts = Workouts.query.all()

            response_body = [workout.to_dict(rules=('-users.workouts', '-user_workouts')) for workout in workouts]
            return make_response(response_body, 201)

        except ValueError:
            rb = {
                "errors": ["validation errors"]
                }
            return make_response(rb, 400)
    def delete(self, u_id, w_id):
        user = User.query.filter(User.id == u_id).first()
        workout = Workouts.query.filter(Workouts.id == w_id).first()

        if user and workout:
            if workout in user.workouts:
                user.workouts.remove(workout)
                db.session.commit()
                return make_response({}, 204)
            else:
                return make_response({"error": "Workout not associated with user"}, 404)
        else:
            return make_response({"error": "User or Workout not found"}, 404)

api.add_resource(UserWorkout,'/users/<int:u_id>/<int:w_id>')

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
            

            if not all([img ,name,price , info]):
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

class AllRatings(Resource):

    def get(self):
        response_body = [rating.to_dict() for rating in Ratings.query.all()]
        return make_response(response_body,200)
    def post(self):
        try:
            
            # Ensure required fields are present in the request
            # id = request.json.get('id')
            rating = request.json.get('rating')
            product_id = request.json.get('product_id')
            
            

            if not all([rating,product_id]):
                raise ValueError("Missing required fields")

            new_r = Ratings(
                
                rating=rating,
                product_id=product_id,
            )
            db.session.add(new_r)
            db.session.commit()

            # Assuming to_dict() method is defined in your Mission model
            rb = new_r.to_dict(rules = ())
            return make_response(rb, 201)

        except ValueError:
            rb = {
                "errors": ["validation errors"]
                }
            return make_response(rb, 400)

api.add_resource(AllRatings, '/ratings')

class AllAbout(Resource):

    def get(self):
        about = About.query.all()

        response_body = [about.to_dict(rules=()) for about in about]
        return make_response(response_body,200)
    def post(self):
        try:
            
            # Ensure required fields are present in the request
            # id = request.json.get('id')
            about = request.json.get('about')
            
            
            

            if not all([about]):
                raise ValueError("Missing required fields")

            new_a = About(
                
                about = about
                
            )
            db.session.add(new_a)
            db.session.commit()

            # Assuming to_dict() method is defined in your Mission model
            rb = new_a.to_dict(rules = ())
            return make_response(rb, 201)

        except ValueError:
            rb = {
                "errors": ["validation errors"]
                }
            return make_response(rb, 400)

api.add_resource(AllAbout, '/about')

class AboutById(Resource):
    def get(self,id):
        
        about = About.query.filter(About.id == id).first()

        if about:
            response_body = about.to_dict(rules = ())
            return make_response(response_body,200)
        else:
            response_body = {
                "error": "User not found"
            }
            return make_response(response_body,404)
    
    def delete(self, id ):
        about = Workouts.query.filter(Workouts.id == id).first()

        if about:
            db.session.delete(about)
            db.session.commit()
            response_body = {}
            return make_response(response_body, 204)
        else:
            response_body = {
                "error": "User not found"
            }
            return make_response(response_body,404)
    def patch(self, id):
        about = About.query.filter(About.id == id).first()

        if about:
            try:
                # Get the data from the PATCH request
                data = request.json

                # Update user attributes if present in the request
                if 'about' in data:
                    about.about = data['about']

                # Commit changes to the database
                db.session.commit()

                # Return the updated user
                response_body = about.to_dict(rules=())
                return make_response(response_body, 200)

            except ValueError:
                response_body = {
                    "error": "Invalid data in the request"
                }
                return make_response(response_body, 400)
        else:
            response_body = {
                "error": "About info not found"
            }
            return make_response(response_body, 404)
 
    

api.add_resource(AboutById,'/about/<int:id>')

class AllVideoIDs(Resource):

    def get(self):
        videoID = VideoID.query.all()

        response_body = [videoid.to_dict(rules=()) for videoid in videoID]
        return make_response(response_body,200)
    def post(self):
        try:
            
            # Ensure required fields are present in the request
            # id = request.json.get('id')
            videoCode = request.json.get('videoId')
            
            
            

            if not all([videoCode]):
                raise ValueError("Missing required fields")

            new_v = VideoID(
                
                videoId = videoCode
                
            )
            db.session.add(new_v)
            db.session.commit()

            # Assuming to_dict() method is defined in your Mission model
            rb = new_v.to_dict(rules = ())
            return make_response(rb, 201)

        except ValueError:
            rb = {
                "errors": ["validation errors"]
                }
            return make_response(rb, 400)

api.add_resource(AllVideoIDs, '/videoid')

class VideoById(Resource):
    def get(self,id):
        
        video = VideoID.query.filter(VideoID.id == id).first()

        if video:
            response_body = video.to_dict(rules = ())
            return make_response(response_body,200)
        else:
            response_body = {
                "error": "User not found"
            }
            return make_response(response_body,404)
    
    def delete(self, id ):
        video = VideoID.query.filter(VideoID.id == id).first()

        if video:
            db.session.delete(video)
            db.session.commit()
            response_body = {}
            return make_response(response_body, 204)
        else:
            response_body = {
                "error": "video id not found"
            }
            return make_response(response_body,404)
    def patch(self, id):
        
        video = VideoID.query.filter(VideoID.id == id).first()

        if video:
            try:
                # Get the data from the PATCH request
                data = request.json

                # Update user attributes if present in the request
                if 'videoId' in data:
                    video.videoId = data['videoId']
                else:
                    response_body = {
                        "error": "there is no videoId in your request"
                    }
                # Commit changes to the database
                db.session.commit()

                # Return the updated user
                response_body = video.to_dict(rules=())
                return make_response(response_body, 200)

            except ValueError:
                response_body = {
                    "error": "Invalid data in the request"
                }
                return make_response(response_body, 400)
        else:
            response_body = {
                "error": "Video Id was not found"
            }
            return make_response(response_body, 404)
 
    

api.add_resource(VideoById,'/videoid/<int:id>')





if __name__ == '__main__':
    app.run()