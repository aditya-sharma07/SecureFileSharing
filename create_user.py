from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    ops_user = User(
        email="ops@example.com",
        password=generate_password_hash("opsuserpassword"),
        role="ops",
        is_verified=True
    )

    db.session.add(ops_user)
    db.session.commit()
    print(" Ops user created.")
