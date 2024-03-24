import bcrypt


def hash_password(pw: str):
    pw_bytes = pw.encode('utf-8')
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pw_bytes, salt).decode('utf-8')


def check_password(pw: str, stored_pw: bytes):
    return bcrypt.checkpw(pw.encode('utf-8'), stored_pw.encode('utf-8'))
