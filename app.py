import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import Movie, Actor, setup_db
from auth import AuthError, requires_auth


def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  with app.app_context():
    setup_db(app)
  CORS(app)

  return app

APP = create_app()


#----------------------------------------------------------------------------#
# Routes
#----------------------------------------------------------------------------#

'''
API endpoint to handle GET requests for details of all Movies
This endpoint will be accessible to all persons
'''
@APP.route('/movies', methods=['GET'])
def get_movies():
    try:
        movies = Movie.query.all()
        if len(movies) == 0:
            abort(404)
        else:
            movies_list = [movie.format() for movie in movies]
            return jsonify({
                'success': True,
                'movies': movies_list
            }), 200
    except:
        abort(422)


'''
API endpoint to handle GET requests for details of all Actors
This endpoint will be accessible to all persons
'''
@APP.route('/actors', methods=['GET'])
def get_actors():
    try:
        actors = Actor.query.all()
        if len(actors) == 0:
            abort(404)
        else:
            actors_list = [actor.format() for actor in actors]
            return jsonify({
                'success': True,
                'actors': actors_list
            }), 200
    except:
        abort(422)


'''
API endpoint to Create a new Movie
This endpoint will be accessible to only authorized persons
'''
@APP.route('/movies', methods=['POST'])
@requires_auth('post:movies')
def create_movie(token):
    body = request.get_json()

    if 'title' in body and 'release_date' in body:
        movie_title = body.get('title')
        movie_release_date = body.get('release_date')
        new_movie = Movie(
            title = movie_title,
            recipe = movie_release_date
        )
        try:
            new_movie.insert()
            return jsonify({
                'success': True,
                'movies': new_movie.format()
            }), 200
        except:
            abort(422)
    else:
        abort(400)


'''
API endpoint to Create a new Actor
This endpoint will be accessible to only authorized persons
'''
@APP.route('/actors', methods=['POST'])
@requires_auth('post:actors')
def create_actor(token):
    body = request.get_json()

    if 'name' in body:
        actor_name = body.get('name')
        actor_age = body.get('age')
        actor_gender = body.get('gender')
        new_actor = Actor(
            name = actor_name,
            age = actor_age,
            gender = actor_gender
        )
        try:
            new_actor.insert()
            return jsonify({
                'success': True,
                'actors': new_actor.format()
            }), 200
        except:
            abort(422)
    else:
        abort(400)


'''
API endpoint to Update an existing Movie data
This endpoint will be accessible to only authorized persons
'''
@APP.route('/movies/<int:id>', methods=['PATCH'])
@requires_auth('patch:movies')
def update_movie(token, id):
    body = request.get_json()

    try:
        # Get the Movie to be updated
        existing_movie = Movie.query.get(id)
        
        if existing_movie is None:
            abort(404)
        else:
            existing_movie.title = body.get('title')
            existing_movie.release_date = body.get('release_date')
            existing_movie.update()
            return jsonify({
                'success': True,
                'movies': existing_movie.format()
            }), 200
    
    except:
        abort(422)


'''
API endpoint to Update an existing Actor data
This endpoint will be accessible to only authorized persons
'''
@APP.route('/actors/<int:id>', methods=['PATCH'])
@requires_auth('patch:actors')
def update_actor(token, id):
    body = request.get_json()

    try:
        # Get the Actor to be updated
        existing_actor = Actor.query.get(id)
        
        if existing_actor is None:
            abort(404)
        else:
            existing_actor.name = body.get('name')
            existing_actor.age = body.get('age')
            existing_actor.gender = body.get('gender')
            existing_actor.update()
            return jsonify({
                'success': True,
                'actors': existing_actor.format()
            }), 200
    
    except:
        abort(422)


'''
API endpoint to Delete a Movie
This endpoint will be accessible to only authorized persons
'''
@APP.route('/movies/<int:id>', methods=['DELETE'])
@requires_auth('delete:movies')
def delete_movie(token, id):
    try:
        movie = Movie.query.filter(Movie.id == id).one_or_none()
        if movie is None:
            abort(404)
        movie.delete()
        return jsonify({
            'success': True,
            'delete': id
        }), 200
    except:
        abort(422)


'''
API endpoint to Delete an Actor
This endpoint will be accessible to only authorized persons
'''
@APP.route('/actors/<int:id>', methods=['DELETE'])
@requires_auth('delete:actors')
def delete_actor(token, id):
    try:
        actor = Actor.query.filter(Actor.id == id).one_or_none()
        if actor is None:
            abort(404)
        actor.delete()
        return jsonify({
            'success': True,
            'delete': id
        }), 200
    except:
        abort(422)


#----------------------------------------------------------------------------#
# Error Handlers
#----------------------------------------------------------------------------#

'''
Example error handling for unprocessable entity
'''
@APP.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "Unprocessable"
    }), 422


'''
Error Handler for Resource Not Found Error
'''
@APP.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "Resource Not Found"
    }), 404


'''
Error Handler for Bad Request Error
'''
@APP.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "Bad Request"
    }), 400


'''
Error Handler for AuthError
'''
@APP.errorhandler(AuthError)
def authentication_problem(error):
    return jsonify({
        "success": False,
        "error": error.status_code,
        "message": error.error.get('description')
    }), error.status_code


if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)