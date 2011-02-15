#!/bin/sh
find . -name '*.py' -not -path '*/migrations/*' -not -name '_generated_media_names.py' -not -name 'manage.py' -exec pep8 {} \;

