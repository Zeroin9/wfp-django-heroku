import uuid
from django.http import JsonResponse
from .models import Token

# check valid of token
def check_auth(token):
    if token is None:
        return False
    same_tokens = Token.objects.filter(token=token)
    if len(same_tokens) == 0:
        return None
    return True

# generate new unique token
def generate_new_token():
    new_token = str(uuid.uuid4())
    same_tokens = Token.objects.filter(token=new_token)
    if len(same_tokens) > 0:
        return generate_new_token()
    else:
        tokenInstance = Token(token=new_token)
        tokenInstance.save()
        return new_token

# Decorator for function with auth
def auth_need(function):
    def wrapper(request):
        token = request.headers.get('AuthToken')
        if token is None:
            return JsonResponse({'error':'Cant find AuthToken'}, status=400)
        is_valid = check_auth(str(token))
        if is_valid is True:
            return function(request)
        else:
            return JsonResponse({'error':'Token is invalid'}, status=401)
    return wrapper