import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from .extensions import paginate_questions

from models import setup_db, Question, Category




def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  CORS(app, resources={r"/api/*": {"origins": "*"}})

  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST,PATCH, DELETE, OPTIONS')
    return response




  @app.route('/categories')
  def categories():
    try:
      categories = Category.query.order_by(Category.id).all()

      if categories is None:
        abort(404)

      return jsonify({
        'categories': {category.id: category.type for category in categories}
      })

    except:
      abort(404)


  

  # Get questions
  @app.route('/questions')
  def questions():

    questions = Question.query.order_by(Question.id).all()
    current_questions = paginate_questions(request, questions)

    categories = Category.query.order_by(Category.id).all()
    

    if len(current_questions) == 0:
      abort(404)


    current_category = {}

    for item in current_questions:

      current_category = item['category']

   
    
    return jsonify({
      'questions': current_questions,
      'total_questions': len(questions),
      'current_category': current_category,
      'categories': {category.id: category.type for category in categories}
    })





 
  @app.route('/delete_question/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):

    try:
      question = Question.query.filter(Question.id==question_id).one()

      if question is None:
        abort(404)

      question.delete()
      
      questions = Question.query.order_by(Question.id).all()
      current_questions = paginate_questions(request, questions)

      return jsonify({

      'questions': current_questions,
      'total_questions': len(Question.query.all()),
      'deleted': question_id
      
      })
    except:
      abort(422)






  @app.route('/questions', methods=['POST'])
  def create_question():

    question = request.get_json()

    if not ('question' in question 
            and 'answer' in question 
            and 'difficulty' in question 
            and 'category' in question):

            abort(422)


    answer = question.get('answer', None)
    category = question.get('category', None)
    new_question = question.get('question', None)
    difficulty = question.get('difficulty', None)


    try:
      new_question = Question(question=new_question, answer=answer,
                             category=category, difficulty=difficulty)
      new_question.insert()
      
      
     

      return jsonify({

      'created': new_question.id,
      'total_questions': len(Question.query.all())
      
      })
    except:
      abort(422)




  # Get questions based on a search term.
  @app.route('/questions/search', methods=['POST'])
  def search():
    

    try:
      
      body = request.get_json()
      search = body.get('searchTerm', None)
      
      if search is None:
        abort(404)
      
      result = Question.query.filter(Question.question.ilike(f'%{search}%')).all()
      return jsonify({
      'questions': [question.format() for question in result],
      'total_questions': len(result),
      'current_category': None
      })

    except:
      abort(404)




  
  
  #Get questions based on category. 
  @app.route('/categories/<int:category_id>/questions')
  def get_question_by_category(category_id):
    try:
      
      result = Question.query.filter(Question.category == category_id).all()


      return jsonify({

      'questions': [question.format() for question in result],
      'total_questions': len(Question.query.all()),
      'current_category': category_id

    })
    except:
      abort(404)
      
      
  
  #A POST endpoint to get questions to play the quiz
  @app.route('/play_quiz', methods=['POST'])
  def play_quiz():

    try:

      body = request.get_json()

      if not ('quiz_category' in body and 'previous_questions' in body):
        abort(422)
        
      category = body.get('quiz_category', None)
      previous_questions = body.get('previous_questions', None)

      if category['type'] == 'click':
        questions = Question.query.filter(Question.id.notin_((previous_questions))).all()
      else:
        questions = Question.query.filter_by(category=category['id']).filter(Question.id.notin_((previous_questions))).all()

      new_question = questions[random.randrange(0, len(questions))].format() if len(questions) > 0 else None

      return jsonify({
        
        'question': new_question
            })

    except:
      abort(422)

        




  # error handlers for all expected errors 
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
        "success": False, 
        "error": 404,
        "message": "Not found"
        }), 404


  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      "success": False, 
      "error": 422,
      "message": "unprocessable"
      }), 422


  return app

    