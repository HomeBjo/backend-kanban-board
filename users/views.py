from django.shortcuts import render
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response


class LoginView(ObtainAuthToken):
    """
     A view for handling user authentication and providing a token upon successful login.

    This view extends the `ObtainAuthToken` and overrides the `post` method to validate the user credentials
    and return an authentication token, user ID, and email address.
    """
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })