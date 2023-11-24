import jwt, os

def decode_jwt(token):
    try:

        token = token.replace('Bearer ', '')

        payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
    
