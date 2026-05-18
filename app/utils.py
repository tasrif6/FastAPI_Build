from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()

def hash_password(password: str):
    return password_hash.hash(password)

def verify_password(normal_password, hashed_password):
    return password_hash.verify(normal_password, hashed_password)