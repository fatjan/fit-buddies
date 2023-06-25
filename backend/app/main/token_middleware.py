from flask import request, jsonify
from functools import wraps
import jwt

# Define the middleware function
def jwt_middleware(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Get the Authorization header from the request
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({'message': 'Authorization header is missing'}), 401

        # Check if the header starts with 'Bearer' and extract the token
        if not auth_header.startswith('Bearer '):
            return jsonify({'message': 'Invalid authorization header'}), 401

        token = auth_header.split(' ')[1]
        try:
            # Verify and decode the JWT token
            decoded_token = jwt.decode(token, 'your-secret-key', algorithms=['HS256'])

            # Retrieve the user ID from the decoded token
            user_id = decoded_token['user_id']

            # Pass the user ID to the decorated endpoint function
            kwargs['user_id'] = user_id

            # Continue with the endpoint function
            return f(*args, **kwargs)

        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token'}), 401

    return decorated_function
