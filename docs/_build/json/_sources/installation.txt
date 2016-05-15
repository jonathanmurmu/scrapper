Installation:
-------------------------------

1. Create a separate virtual environment with python 3.4, and activate it.

		$ virtualenv -p /usr/bin/python3 /path/to/enviornment/directory/
		$ source /path/to/enviornment/directory/bin/activate

2. Clone the project to a folder where you would like the store the project.

		$ git clone https://github.com/jonathanmurmu/scrapper.git

3. Create a database named 'scapper'

4. Write the following configuration in 'settings.py':
	
		DATABASES = {

	    'default': {
	        'ENGINE': 'django.db.backends.mysql',
	        'NAME': 'scrapper',
	        'USER': 'mysql client username',
	        'PASSWORD': 'mysql client password',
	        'HOST': '',
	        'PORT': '',
	    	}
		}

		EMAIL_HOST = 'your email host'
		EMAIL_HOST_USER = 'email username'
		EMAIL_HOST_PASSWORD = 'email password'
		EMAIL_PORT = 587
		EMAIL_USE_TLS = True



5. Run the following command in terminal to create the required tables for the project.

		$ python manage.py makemigrations
		$ python manage.py migrate

6. Start the server.

		$ python manage.py runserver

7. Type the following url in the browser to execute the project.

		http://localhost:8000/
