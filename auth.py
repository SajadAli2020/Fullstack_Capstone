import json
from flask import request, _request_ctx_stack
from functools import wraps
from jose import jwt
from urllib.request import urlopen
# import pdb

AUTH0_DOMAIN = 'balanafsnd.us.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'CoffeeShop'

## AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


## Auth Header
'''
It should raise an AuthError if either header is missing or malformed,
otherwise return the token part of the request header
'''
def get_token_auth_header():
   auth_header = request.headers.get('Authorization', None)
   if not auth_header:
       raise AuthError({
           'code': 'Invalid_Claim',
           'description': 'Authorization Header Not Found'
       }, 401)
   
   header_parts = auth_header.split()
   if len(header_parts) == 0:
        raise AuthError({
            'code': 'Invalid_Claim',
            'description': 'Invalid Token Header.'
        }, 401)
   
   if header_parts[0].lower() != 'bearer':
       raise AuthError({
           'code': 'Invalid_Claim',
           'description': 'Authorization Header must start with "Bearer"'
       }, 401)
   elif len(header_parts) == 1:
       raise AuthError({
           'code': 'Invalid_Claim',
           'description': 'Token Not Found in the Header'
       }, 401)
   elif len(header_parts) > 2:
       raise AuthError({
           'code': 'Invalid_Claim',
           'description': 'Authorization Header must be Bearer Token'
       }, 401)
   
   return header_parts[1]


'''
It should raise an AuthError if either permissions array is missing from payload,
or permission string is missing from permissions array. Otherwise return true
'''
def check_permissions(permission, payload):
    if 'permissions' not in payload:
        raise AuthError({
            'code': 'Invalid_Claim',
            'description': 'Permissions array is missing from JWT'
        }, 400) 
    
    if permission not in payload['permissions']:
        raise AuthError({
            'code': 'Unauthorized',
            'description': 'Permission Not Found'
        }, 403) 
    return True


'''
It should take a JWT token as Input and then verify that
it is an Auth0 token. After verification, it should decode
the token payload, validate the claims and returns the 
decoded token payload
'''
def verify_decode_jwt(token):
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    #pdb.set_trace()
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'Invalid_Header',
            'description': 'Authorization malformed'
        }, 401)
    
    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )
            return payload
        
        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'Token_Expired',
                'description': 'Token already Expired'
            }, 401)
        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'Invalid_Claims',
                'description': 'Incorrect Claims. Please, check the audience and issuer'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'Invalid_Header',
                'description': 'Unable to parse Authentication Token'
            }, 400)
    
    raise AuthError({
        'code': 'Invalid_Header',
        'description': 'Unable to find the appropriate key'
    }, 400)

'''
It should take "permission (e.g. 'post:movie')" as Input, and will use the
    get_token_auth_header method to get the token
    verify_decode_jwt method to decode the jwt
    check_permissions method to validate claims and check the requested permission
    and then return the decorator which passes the decoded payload to the decorated method
'''
def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            #pdb.set_trace()
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator