Note: This contains my virtualenv build which is why a bin, include and lib file
are here in addition to the src file. There is also a newly added static_in_env
folder which holds external files (images, css, js) that our program will use.
From my reading this should help make the process of migrating the website to an actual
server easier.

Steps for installing:
1. Activate the virtualenv (*a)
  >source bin/activate
2. Move to the base directory for the website (src)
  cd src
3. Move all the static files into the static folder 
  >python3 manage.py collectstatic
4. Run the server
  >python3 manage.py runserver

  (*a) - I have had some trouble with the virtualenv in the past, and it's respective
         files may need to be removed from this in the future. For me to get this to
         work, I've simply deleted the bin, include, and lib directories, and started
         a new virtualenv from scratch in the current directory. 
          
          >rm -r bin include lib
          >virtualenv -p python3 .

Database Setup:
This was all done on my Mac, so it may be different for a Windows machine.
1. Install postgresql if you haven't
   >sudo apt-get install python-pip python-dev libpq-dev postgresql postgresql-contrib
2. In the virtualenv, install psycopg2
   >pip install django psycopg2
3. Set up the postgresql user, myprojectuser with CREATEDB permissions
   >psql
   >CREATE USER myprojectuser WITH PASSWORD 'password' CREATEDB;
   >\q  #to exit the psql interactive terminal
4. Run the script to create the database
   >./marsdb.sh
5. Migrate the database
   >python manage.py migrate
6. Add samples to the database
   #Add command here once dataParser is done
7. Create your admin user
   >python manage.py createsuperuser
