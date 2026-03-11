import os
from flask_admin import Admin
from models import db, User, Character, Race, ClassBase, Zone, Location, Friendship
from flask_admin.contrib.sqla import ModelView

def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap3')


    class CharacterAdmin(ModelView):
        form_columns = [
            "name",
            "level",
            "first_account",
            "race_choice",
            "class_base_choice",
            "location_character"
        ]

    class LocationAdmin(ModelView):
        form_columns = [
            "x",
            "y",
            "z",
            "location_zone"
        ]
    
    # Add your models here, for example this is how we add a the User model to the admin
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Race, db.session))
    admin.add_view(ModelView(ClassBase, db.session))
    admin.add_view(ModelView(Zone, db.session))
    admin.add_view(LocationAdmin(Location, db.session))
    admin.add_view(ModelView(Friendship, db.session))
    admin.add_view(CharacterAdmin(Character, db.session))

    # You can duplicate that line to add mew models
    # admin.add_view(ModelView(YourModelName, db.session))