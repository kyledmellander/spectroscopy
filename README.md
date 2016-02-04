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
