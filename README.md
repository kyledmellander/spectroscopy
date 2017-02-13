See the site at http://spectro.geol.wwu.edu

About the site:
   - The primary use of the site is to search through a database containing VIS-NIR spectroscopy data,
     select samples from the search results, and then view the samples as a line/scatter plot. The users
     can also choose to download selected spectra in a zip file to perform any additional analysis. Some metadata
     about the samples, including a sample description is also available to view through the site, and is included
     with the downloaded sample data. 

Database Setup:
1. Install postgresql if you haven't
   >sudo apt-get install python-pip python-dev libpq-dev postgresql postgresql-contrib
  
2. Install psycopg2

3. Set up the postgresql server with a user, myprojectuser with CREATEDB permissions, and set the password as specified
   in the settings.py file located in the djangoproject directory.
   >psql
   >CREATE USER myprojectuser WITH PASSWORD 'password' CREATEDB;
   >\q  #to exit the psql interactive terminal
   
4. Prepare database migrations
   >python manage.py makemigrations -initdb
   
5. Migrate the database
   >python manage.py migrate
