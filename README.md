[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/ecFNqaXc)

# Week 21 Assignment - Twitter Clone Backend App using Flask (Visit API Documentation at https://documenter.getpostman.com/view/29042682/2s9YeD7Cci )

Build a simplified Twitter like version using flask. This project includes implementation of registration and login functionality, posting tweets, following or unfollowing users and obtaining user profiles. Flask is utilized for routing, apis, blueprints, HTTP methods. Integrate Postgresql in Supabase using SQLAlchemy. Token based authentication is implemented too.

Here are libraries in flask that being used for this twitter clone flask app :

1. flask 
2. flask-sqlalchemy 
3. pyscopg2-binary 
4. flask-bcrypt 
5. pyjwt 
6. marshmallow

Before set up some packages and develop the flask app especially in Visual Studio Code, Please do some preliminary steps below:

1. Please add Python 311 Script first to the PATH (for Windows user only).
2. For example add this : "C:\Users\Aldi Andalan\AppData\Roaming\Python\Python311\Scripts" into PATH
3. In windows explorer, click -> this pc -> advance system settings -> advance -> environment variable -> edit path
4. Then put for instance "C:\Users\Aldi Andalan\AppData\Roaming\Python\Python311\Scripts" into the PATH and click ok.
5. After that, execute these commands in terminal, windows, command prompt or PowerShell in Visual Studio Code:  

Here are some set ups before developing the flask app

#### Upgrade Python
``` 
python.exe -m pip install --upgrade pip --user
```
#### Install pipenv
``` 
pip install pipenv --user
```
#### Install flask
``` 
pip install flask --user 
```
#### Python Versioning
``` 
pipenv --python 3.11  # or replace with your Python version
```
#### Activate viertual environment (venv)
``` 
pipenv shell
```
#### Install Packages
``` 
pipenv install flask flask-sqlalchemy pyscopg2-binary flask-bcrypt pyjwt marshmallow
```
After all packages are installed, you can clone my codes and try running the apps. But before that make sure python interpreter selector is correct. You can check that in Visual Studio Code by pressing **Ctrl+Shift+P** all together simultaneously, then choose Python: Interpreter Selector and the choose the one with **venv** or virtual environment. It helps Visual Studio recognized your installed packages on pipfile that is obtained by setting up python and flask library above.

If all thet's steps are done, voila, you can run the flask application, run the flask application by using these commands in terminal:

#### Run Flask App
``` 
pipenv shell
```

``` 
pipenv run flask run --debug
```
or
``` 
flask run --debug
```

After all of that, you can check or testing the APIs endpoints in postman app. Please visit API Documentation at https://documenter.getpostman.com/view/29042682/2s9YeD7Cci to get clearer examples for body request in APIs enpoint which is used in this app.

for further question please contact author at andalanaldi@gmail.com