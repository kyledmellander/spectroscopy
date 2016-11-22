Database Setup:
1. Install postgresql if you haven't
   >sudo apt-get install python-pip python-dev libpq-dev postgresql postgresql-contrib
2. Install psycopg2
3. Set up the postgresql user, myprojectuser with CREATEDB permissions
   >psql
   >CREATE USER myprojectuser WITH PASSWORD 'password' CREATEDB;
   >\q  #to exit the psql interactive terminal
4. Run the script to create the database
   >./marsdb.sh
5. Migrate the database
   >python manage.py migrate
6. Create your admin user
   >python manage.py createsuperuser
7. Start up the server
   >python manage.py runserver
8. Login with the information you created in createsuperuser
9. With the superuser, create any additional admin users.
10. Upload the spectroscopy data
11. View the data!
