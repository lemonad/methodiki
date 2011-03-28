Prerequisites
------------
*  Python
*  SQLite3 *(default)* or other database backend.
*  [Sass](http://sass-lang.com/) for generating style sheets.
*  Memcached for caching *(optional)*.

Setup
-----
### Install Haml/Sass:
    $ gem install haml

### Clone project
    $ git clone git@github.com:lemonad/methodiki.git   # (or equivalent)
    $ cd methodiki
    $ virtualenv --no-site-packages .
    $ source bin/activate
    $ pip install -r requirements.txt
    $ pip install -r requirements-mysql.txt            # (optional)
    $ cd methodiki
    $ cp local_settings.example local_settings.py      # (optional)
    $ python manage.py syncdb --settings development
    $ python manage.py migrate --settings development
    $ python manage.py compilemessages
    $ python manage.py generatemedia --settings development

Development server
--------------------------
    $ python manage.py runserver --settings development

Production server
-------------------------
* Map `/media/` to `./methodiki/media/` *(media uploads, thumbnails, etc.)*
* Map `/static/` to `./methodiki/_generated_media/` *(css, javascipt, etc.)*
* Start server:

    $ python manage.py runserver --settings production
