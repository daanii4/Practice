from passlib.context import CryptContext

# Create a password context for hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Function to hash a password
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# Example usage
plain_password = "Oghenetega2004$"  # Replace with your actual password
hashed_password = get_password_hash(plain_password)

print("Hashed Password:", hashed_password)
