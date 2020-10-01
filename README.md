# project_repo
A starter project for Django 3.0
## Features
Features a custom User and Profile management, user messages, a Blog and a
Nested Pages app. Uses Filebrowser and Django Private Storage for handling
images and files and Streamblocks to compose pages.
## Install
Clone the repository, use requirements.txt to install dependencies. Copy secrets_move_out_of_repo.json out of repository, rename to secrets.json and fill
in the global settings. Modify project/static/favicon.ico and logo.png for
custom branding. Migrate, collectstatic and createsuperuser.
## Deployment
In production use manpro.py instead of manage.py and point server to
wsgi_prod.py instead of wsgi.py.
## User management
User is extended by a Profile model with additional info. New users must be
granted 'Can add user upload' permission to comment blog articles. 'Trusted'
group with such permission is created on setup (add your own permissions to
this group). If staff member has access to Profile but not to User, he can still
add user to 'Trusted' group by flagging Profile to is_trusted. This attribute is
false by default, but you can change this globally for newly created users
changing the IS TRUSTED BY DEFAULT setting.
