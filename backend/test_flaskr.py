import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_all_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data)


    def test_404_sent_requesting_non_existing_category(self):
        res = self.client().get('/categories/10000000000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found')


    def test_get_paginated_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        categories = Category.query.order_by(Category.id).all()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['questions'])
        self.assertTrue(data['current_category'])
        self.assertTrue(data['categories'])


    def test_404_sent_requesting_questions_beyond_valid_page(self):
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found')


    def test_delete_question(self):
        question = Question(question='test question', answer='test answer',
                            difficulty=1, category=1)
        question.insert()
        question_id = question.id

        res = self.client().delete(f'/delete_question/{question_id}')
        data = json.loads(res.data)


        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['deleted'], question_id)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        

    def test_422_sent_deleting_non_existing_question(self):
        res = self.client().delete('/delete_question/3000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')



    def test_create_question(self):

        new_question = {

            'question': 'Where Italy is located?',
            'answer': 'Europe',
            'difficulty': 3,
            'category': 2
        }

        total_questions_before = len(Question.query.all())
        res = self.client().post('/questions', json=new_question)
        data = json.loads(res.data)
        total_questions_after = len(Question.query.all())

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['created'])

        self.assertEqual(data['total_questions'], total_questions_before + 1)


    def test_422_create_question(self):
        new_question = {
            'question': 'Where Italy is located?',
            'answer': 'Europe',
            
            'category': 2
        }
        res = self.client().post('/questions', json=new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")


    def test_search_questions(self):
        search = {'searchTerm': 'n'}
        res = self.client().post('questions/search', json=search)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertIsNotNone(data['questions'])
        self.assertIsNotNone(data['total_questions'])



    def test_404_search_question(self):
        search = {
            'search': '',
        }
        res = self.client().post('questions/search', json=search)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Not found")





    def test_get_questions_per_category(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['current_category'])





    def test_404_get_questions_per_category(self):
        res = self.client().get('/categories/a/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Not found")




    def test_play_quiz(self):
        new_quiz = {'previous_questions': [],
                          'quiz_category': {'type': 'Entertainment', 'id': 1}}

        res = self.client().post('/play_quiz', json=new_quiz)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['question'])



    def test_422_play_quiz(self):
        new_quiz = {'previous_questions': []}
        res = self.client().post('/play_quiz', json=new_quiz)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()