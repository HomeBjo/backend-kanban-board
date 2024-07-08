from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
import json

class RegisterView(APIView):
    """
    Handles the registration of a new user.

    This view allows a user to register by providing a username, password, and password confirmation.
    Upon successful registration, a new user is created, and an authentication token is returned.

    Methods:
        post(request): Handles the registration of a new user.

    Parameters:
        request (Request): The HTTP request containing the registration data.

    Returns:
        JsonResponse: A response containing a success message and the authentication token if registration is successful,
                      or an error message if the registration fails.
    """
    @csrf_exempt
    def post(self, request):
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        username = data.get('username')
        password = data.get('password')
        password_confirm = data.get('password_confirm')

        if not username or not password or not password_confirm:
            return JsonResponse({'error': 'Missing fields'}, status=400)

        if password != password_confirm:
            return JsonResponse({'error': 'Passwords do not match'}, status=400)

        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'Username already exists'}, status=400)

        user = User.objects.create_user(username=username, password=password)
        user.save()

        token, created = Token.objects.get_or_create(user=user)

        return JsonResponse({'message': 'User created successfully', 'token': token.key}, status=201)


class LoginView(APIView):
    """
    Handles the authentication of a user.

    This view allows a user to log in by providing a username and password.
    Upon successful authentication, an authentication token is returned along with user details.

    Methods:
        post(request): Handles the authentication of a user.

    Parameters:
        request (Request): The HTTP request containing the login data.

    Returns:
        JsonResponse: A response containing a success message, the authentication token, and user details if authentication is successful,
                      or an error message if authentication fails.
    """
    @csrf_exempt
    def post(self, request):
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return JsonResponse({'error': 'Missing fields'}, status=400)

        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            return JsonResponse({
                'success': True,
                'message': 'Login successful',
                'token': token.key,
                'user_id': user.pk,
                'email': user.email
            })
        else:
            return JsonResponse({'success': False, 'error': 'Invalid credentials'}, status=400)


class UserDetailView(APIView):

    def delete(self, request, user_id):     
        """
        Deletes an existing task for the authenticated user.

        Parameters:
            request (Request): The HTTP request.
            pk (int): The primary key of the task to be deleted.
            format (str, optional): The format of the response.

        Returns:
            Response: A response indicating the result of the delete operation.
        """
        try:
            user = User.objects.get(id=user_id)
            user.delete()
            return JsonResponse({'message': 'User deleted successfully'}, status=200)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User does not exist'}, status=404)
        

    def patch(self, request, user_id):
        """
        Updates an existing subtask for the authenticated user.

        Parameters:
            request (Request): The HTTP request containing updated subtask data.
            task_id (int): The primary key of the task.
            pk (int): The primary key of the subtask.
            format (str, optional): The format of the response.

        Returns:
            Response: A response containing the serialized updated subtask.
        """
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User does not exist'}, status=404)

        data = json.loads(request.body)
        username = data.get('username', user.username)
        password = data.get('password', None)

        user.username = username
        if password:
            user.set_password(password)
        user.save()

        return JsonResponse({'message': 'User updated successfully'}, status=200)
