# project_repo
A starter project for Django 3.0
## Features
Features a custom User and Profile management, user messages, a Blog and a Nested Pages app.
## Install
Clone the repository, use requirements.txt to install dependencies. Copy secrets_move_out_of_repo.json out of repository, rename to secrets.json and fill in the global settings (some work both in dev and production, others only in production).
Migrate, collectstatic and createsuperuser.
## Deployment
In production use manpro.py instead of manage.py and point server to wsgi_prod.py instead of wsgi.py.
