import json
from functools import wraps

from django import http
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt

User = get_user_model()


def _json_response(status, ok, message, **body):
    bag = {
        'ok': ok,
        'message': message or '',
        'body': body
    }
    return http.HttpResponse(json.dumps(bag), status=status)


def required_method(*methods):
    def required_methods_decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            if request.method in methods:
                return func(request, *args, **kwargs)
            else:
                return _json_response(405, False, "method not supported")

        return wrapper

    return required_methods_decorator


@csrf_exempt
@required_method("POST")
def signup(request):
    try:
        bag = json.loads(request.body, 'utf-8')
        username = bag['username']
        if len(username) < 5:
            raise Exception("username too short")
        password = bag['password']
        if len(password) < 8:
            raise Exception("password too short")
        user = User.objects.create_user(username, password=password, token=Token.generate())
        return _json_response(200, True, "created", **{'username': user.username, 'token': user.token})
    except Exception as e:
        return _json_response(400, False, str(e))


@csrf_exempt
@required_method("POST")
def login(request):
    try:
        bag = json.loads(request.body, 'utf-8')
        username = bag['username']
        user = User.objects.get(username=username)
        user.token = User.generate_token()
        user.save()
        return _json_response(200, True, "logged in", **{'username': user.username, 'token': user.token})
    except Exception as e:
        return _json_response(400, False, str(e))


@csrf_exempt
@required_method("POST")
def register(request):
    try:
        bag = json.loads(request.body, 'utf-8')
        user = User.objects.get(token=bag['token'])
        user.registration_id = bag['registration_id']
        user.save()
        return _json_response(200, True, "registered")
    except Exception as e:
        return _json_response(400, False, str(e))


@required_method("GET")
def user(request):
    try:
        username = request.GET['username']
        user = User.objects.get(username=username)
        return _json_response(200, True, "found", **{'username': user.username})
    except Exception as e:
        return _json_response(400, False, str(e))


@csrf_exempt
@required_method("GET", "POST")
def coords(request):
    try:
        if request.method == 'GET':
            user = User.objects.get(token=request.GET['token'])
            return _json_response(200, True, 'get coords',
                                  **{'latitude': user.latitude, 'longitude': user.longitude, 'altitude': user.altitude})
        elif request.method == 'POST':
            bag = json.loads(request.body, 'utf-8')
            user = User.objects.get(token=bag['token'])
            user.longitude = bag['longitude']
            user.latitude = bag['latitude']
            user.altitude = bag['altitude']
            user.save()
            return _json_response(200, True, "set coords",
                                  **{'latitude': user.latitude, 'longitude': user.longitude, 'altitude': user.altitude})
    except Exception as e:
        return _json_response(400, False, str(e))
