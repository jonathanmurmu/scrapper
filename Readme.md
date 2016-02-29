Scrapper
===============================


Overview:
-------------------------------

Web scrapers are a useful tool for gathering information and putting it into useable form. The contents of a given URL can be merged into a database.

This web application allows user to extract specific product details from ecommerce sites like www.flipkart.com and www.amazon.in. Extracted product details are then displayed in the front end. Information like product name, price, category, product's image and the source website is displayed. The user can click on the particular product to go to its source website page, to view the product's detailed description and buy the product.


Requirements:
-------------------------------

	Python 3.4.3
	MySQL client 1.3.7
	MechanicalSoup 0.4.0
	Pillow 3.1.1
	decorator 4.0.6
	virtualenv
	Django 1.8
	beautifulsoup4 4.4.1
	ipython 4.0.3
	ipython-genutils 0.1.0
	path.py 8.1.2
	pexpect 4.0.1
	pickleshare 0.6
	ptyprocess 0.5
	pytz 2015.7
	requests 2.9.1
	simplegeneric 0.8.1
	six 1.10.0
	traitlets 4.1.0
	wheel 0.24.0


Technologies Used:
-------------------------------

Backend:

	Django 1.8
	MySQL 1.3.7

Front end:

	HTML5
	CSS3
	Bootstrap 3
	jQuery


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
