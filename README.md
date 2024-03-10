# Senior-Project
How to download and run
------------------------------------------------------------------------------------------------------------------------------------------
1. Clone the Github repository in VSCode  
   https://github.com/DanK2002/Senior-Project.git  
2. In git bash, set up a virutal environment. For Windows:  
  	cd \<\<file path to parent folder>>/Senior-Project  
  	python -m venv env  
  	source env/Scripts/activate  
  	pip install Django  
  	pip install Faker  
  	python manage.py makemigrations basic  
  	python manage.py migrate basic  
3. Open the repository in VSCode. It will detect the virtual environment, so allow it to default to the virtual environment you created.  
4. Create a superuser in VSCode terminal using Git Bash.  
	python manage.py createsuperuser  
5. Run the server, go to localhost:8000/admin/ and log in with your super user username and password.  
6. Click on a database to verify that the app was set up correctly.  
7. After verifying proper installation and setup, run the fake data script:
   	python manage.py shell < fakedata_complete.py
