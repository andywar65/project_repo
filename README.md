# project_repo
A starter project for Django 3.0
## Features
Features a custom User and Profile management, user messages, a Blog and a Nested Pages app.
Uses Filebrowser for handling images and Streamblocks to compose pages.
## Install
Clone the repository, use requirements.txt to install dependencies. Copy secrets_move_out_of_repo.json out of repository, rename to secrets.json and fill in the global settings (some work both in dev and production, others only in production). Rename
project/settings/base_sample.py and project/urls_sample.py and project/static/css/base_sample.css
to base.py, urls.py and base.css, add other installed apps, urlpatterns and custom styles.
Migrate, collectstatic and createsuperuser. Stash your customizations before pulling.
## Deployment
In production use manpro.py instead of manage.py and point server to wsgi_prod.py instead of wsgi.py.
