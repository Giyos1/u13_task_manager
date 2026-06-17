import jwt, datetime

SECRET_KEY = 'your_secret_key'
REFRESH_SECRET = 'your_refresh_secret'


def create_tokens(user_id):
    access_payload = {
        'user_id': user_id,
        'type': 'access',
        'exp': datetime.datetime.now() +
               datetime.timedelta(minutes=5)
    }
    refresh_payload = {
        'user_id': user_id,
        'type': 'refresh',
        'exp': datetime.datetime.now() +
               datetime.timedelta(days=7)
    }
    access = jwt.encode(access_payload, SECRET_KEY, 'HS256')
    refresh = jwt.encode(refresh_payload, REFRESH_SECRET, 'HS256')
    return {'access': access, 'refresh': refresh}


def verify_token(token, secret,
                 expected_type='access'):
    try:
        payload = jwt.decode(
            token, secret, algorithms=['HS256']
        )
        if payload.get('type') != expected_type:
            return None
        return payload
    except jwt.ExpiredSignatureError:
        return "Token expired"
    except jwt.InvalidTokenError:
        return "Invalid token"


def refresh_access_token(refresh_token):
    payload = verify_token(
        refresh_token, REFRESH_SECRET,
        expected_type='refresh'
    )
    if not isinstance(payload, dict):
        return {'error': payload}

    # Faqat yangi access token
    new_access = jwt.encode({
        'user_id': payload['user_id'],
        'type': 'access',
        'exp': datetime.datetime.now() + datetime.timedelta(minutes=5)
    }, SECRET_KEY, 'HS256')
    return {'access': new_access}


if __name__ == '__main__':
    print(create_tokens(1))
    # print(verify_token(
    #     "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxMiwidHlwZSI6ImFjY2VzcyIsImV4cCI6MTc4MTcyNzQyOH0.SQ0Feup5gnppoU8Y1hynTGnFIQxRLqxWBs4qZAdbGhM",
    #     SECRET_KEY))
    pass
