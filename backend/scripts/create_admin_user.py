from app.models import User
from app.database import SessionLocal
from app.utils.security import hash_password

def create_admin_user():
    db = SessionLocal()  # Create a new session
    try:
        admin_user = User(
            email="danielemojevbe@gmail.com",
            hashed_password=hash_password("Oghenetega2004$"),
            is_admin=True
        )
        db.add(admin_user)  # Add the admin user to the session
        db.commit()  # Commit the transaction
        print("Admin user created successfully!")
    except Exception as e:
        print(f"Error creating admin user: {str(e)}")
    finally:
        db.close()  # Close the session

if __name__ == "__main__":
    create_admin_user()
