import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

# from flaskr import create_app
from app import create_app
from models import setup_db, Movie, Actor


class CastingAgencyTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client

        #############################################################
        # self.database_name = 'trivia_test'

        # # Secrets are Stored as Environment Variables
        # database_host = os.getenv('DB_HOST')
        # database_user = os.getenv('DB_USER')
        # database_password = os.getenv('DB_PASSWORD')
        # self.database_path = 'postgresql://{}:{}@{}/{}'.format(
        #     database_user,
        #     database_password,
        #     database_host,
        #     self.database_name
        # )
        ############################################################


        # Binds the app to the current context
        # with self.app.app_context():
        #     setup_db(self.app, self.database_path)
        #     self.db = SQLAlchemy()
        #     self.db.init_app(self.app)
        #     # Create all tables
        #     self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    Tests for Successful Operations and Expected Errors.
    """
    def test_get_movies(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])
    

    def test_404_sent_requesting_individual_movie(self):
        res = self.client().get('/movies/2')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')
    

    def test_get_actors(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])
    

    def test_404_sent_requesting_individual_actor(self):
        res = self.client().get('/actors/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')
    
    
    def test_delete_movie(self):
        res = self.client().delete('/movies/2')
        data = json.loads(res.data)

        movie = Movie.query.filter(Movie.id == 2).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 2)
        self.assertEqual(movie, None)
    

    def test_422_sent_if_movie_does_not_exist(self):
        res = self.client().delete('/movies/210')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable')
    

    def test_delete_actor(self):
        res = self.client().delete('/actors/1')
        data = json.loads(res.data)

        actor = Actor.query.filter(Actor.id == 1).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 1)
        self.assertEqual(actor, None)
    

    def test_422_sent_if_actor_does_not_exist(self):
        res = self.client().delete('/actors/121')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable')

    
    def test_create_new_movie(self):
        res = self.client().post('/movies', json={
            'title': 'Raees',
            'release_date': '10-Jan-2020'
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
    

    def test_400_sent_if_insufficient_data_for_movie_creation(self):
        res = self.client().post('/movies', json={'release_date': '01-Feb-2010'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad Request')
    

    def test_create_new_actor(self):
        res = self.client().post('/actors', json={
            'name': 'Shah-Rukh-Khan',
            'age': 48,
            'gender': 'Male'
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
    

    def test_400_sent_if_insufficient_data_for_actor_creation(self):
        res = self.client().post('/actors', json={'gender': 'Male'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad Request')
    
    
    def test_update_existing_movie(self):
        res = self.client().patch('/movies/1', json={
            'title': 'The Raees',
            'release_date': '23-Mar-2020'
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
    

    def test_update_existing_actor(self):
        res = self.client().patch('/actors/1', json={
            'name': 'Salman Khan',
            'age': 51,
            'gender': 'Male'
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
