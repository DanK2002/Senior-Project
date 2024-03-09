# Senior-Project
How to download and run
------------------------------------------------------------------------------------------------------------------------------------------
1. Clone the Github repository in VSCode
   https://github.com/DanK2002/Senior-Project.git
3. In git bash, set up a virutal environment
  For Windows:
  	cd <<file path to parent folder>>/Senior-Project
  	python -m venv env
  	source env/Scripts/activate
  	pip install Django
  	pip install Faker
  	python manage.py makemigrations basic
  	python manage.py migrate basic
5. Open the repository in VSCode. It will detect the virtual environment, so allow it to default to the virtual environment you created.
6. Create a superuser in VSCode terminal
    Use Git Bash Terminal.
	  python manage.py createsuperuser
7. Run the server, go to localhost:8000/admin/ and log in with your super user username and password.
8. Click on a database to verify that the app was set up correctly.
