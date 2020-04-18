# Full Stack Trivia API Backend

Udacity is invested in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a  webpage to manage the trivia app and play the game, but their API experience is limited and still needs to be built out. Trivia is an API provides endpoints to get questions and answer them for entertainment. It also has a quize game to seeing who's the most knowledgeable of the bunch.

The application includes:

1) Display questions - both all questions and by category. Questions show the question, category and difficulty rating by default and can show/hide the answer. 
2) Delete questions.
3) Add questions and require that they include question and answer text.
4) Search for questions based on a text query string.
5) Play the quiz game, randomizing either all questions or within a specific category. 

The code adheres to the PEP 8 style guide

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

The application is run on http://127.0.0.1:5000/ by default.



## API References

### Getting Started

- Base URL: At present this app can only run locally and is not hosted as a base URL.
- Authentication: This version of the application does not require API keys.

### Error Handling

Error are returned as JSON objects in the following format:
```bash

{
    "success": False,
    "error": 400,
    "message": "bad request"
}

```

The API will return two error types when request fail:

- 404: Not Found
- 422: Not processable

## Endpoints

### GET/ questions

- Return a list of questions objects, total_questions, current_category and categories.

- Sample curl http://127.0.0.1.5000/questions

```bash

{
  "categories": {
    "1": "Entertainment", 
    "2": "Adventure"
  }, 
  "current_category": "2", 
  "questions": [
    {
      "answer": "new_answer", 
      "category": "1", 
      "difficulty": null, 
      "id": 2, 
      "question": "new_question"
    }, 
    {
      "answer": "Europe", 
      "category": "2", 
      "difficulty": 3, 
      "id": 3, 
      "question": "Where Italy is located?"
    }, 
    {
      "answer": "new_answer", 
      "category": "1", 
      "difficulty": null, 
      "id": 4, 
      "question": "new_question"
    }],
    "total_questions": 30


```

GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs.

```bash

{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}

```

DELETE '/delete_question/<int:question_id>'

- Delete questions from the database by determining their IDS

Example:

```bash

{

      "questions": [
    {
      "answer": "new_answer", 
      "category": "1", 
      "difficulty": null, 
      "id": 2, 
      "question": "new_question"
    }, 
      'total_questions': 30,
      'deleted': 3
      
      }


```


POST '/questions'

- Add a new question to the database

Example response:

```bash

{
  "created": {
      "answer": "Europe", 
      "category": "2", 
      "difficulty": 3, 
      "id": 3, 
      "question": "Where Italy is located?"
    }, 
  'total_questions': 30
}

```


POST '/questions/search'

- Fetches all questions that matches the search term (case-sensitive)

Example response:

```bash

{
  "current_category": null, 
  "questions": [
    {
      "answer": "Europe", 
      "category": "2", 
      "difficulty": 3, 
      "id": 3, 
      "question": "Where Italy is located?"
    }
  ], 
  
  "total_questions": 1
}

```



GET '/categories/<int:category_id>/questions'


- Get questions based on the passed category

- Request argument: category_id:int

Example response:

```bash

{
  "current_category": 2, 
  "questions": [
    {
      "answer": "Europe", 
      "category": "2", 
      "difficulty": 3, 
      "id": 3, 
      "question": "Where Italy is located?"
    }
  ], 
 
  "total_questions": 2
}

```


POST '/play_quiz'

- retrieve random question from a specified category.


Request argument : {previous_questions: quiz_category: {id:int, type:string}}


Example response:

```bash

{
  "question": {
      "answer": "Europe", 
      "category": "2", 
      "difficulty": 3, 
      "id": 3, 
      "question": "Where Italy is located?"
    }
}

```











REVIEW_COMMENT
```

POST ...
DELETE ...

GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}

```


## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```