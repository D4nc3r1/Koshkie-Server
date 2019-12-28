#  Copyright (c) Code Written and Tested by Ahmed Emad in 28/12/2019, 22:43
from django.contrib.auth import login
from rest_framework import viewsets, views, status
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.models import UserAddressModel, UserProfileModel
from users.permissions import HasProfile
from users.serializers import UserProfileSerializer, UserAddressSerializer


@api_view(['POST'])
def create_user_profile(request):
    """Creates A new user profile and Logs it In.

    Checks if user is authenticated if true, return HTTP 403 Response,
    then it Validates the post data if not valid,
    return HTTP 400 Response, then creates the user and logs him in.
    requires no permissions.

    Arguments:
        request: the request data sent by the user, it is used
                 to get the post data from it to get validated and created,
                 and to log the user in.

    Returns:
        HTTP 201 Response with the JSON data of the created profile.
    """

    if request.user.is_authenticated:
        return Response('User already logged in', status=status.HTTP_403_FORBIDDEN)
    serializer = UserProfileSerializer(data=request.data)
    if serializer.is_valid():
        user_profile = serializer.save()
        login(request, user_profile.account)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_user_profile(request, pk=None):
    """Retrieves the user profile by its pk.

    Checks if a user profile with this pk exist,
    if not, returns HTTP 404 Response.
    requires no permissions.

    Arguments:
        request: the request data sent by the user, it is not used
                 in this view but required by the django framework.
        pk: the id of the user profile that the user want info about,
            it should by an integer.

    Returns:
        HTTP 404 Response if user profile is not found, if not, returns HTTP 200
        Response with the address's JSON data.
    """

    user_profile = get_object_or_404(UserProfileModel, pk=pk)
    serializer = UserProfileSerializer(user_profile)
    return Response(serializer.data)


class UserProfileView(views.APIView):
    """View for the user profile.

    Retrieves, Updates and Deletes a User, requires user authentication.
    """

    permission_classes = (IsAuthenticated, HasProfile)

    def get(self, request):
        """Retrieves the profile of the current user.

        Arguments:
            request: the request data sent by the user, it is used
                     to get the user profile.

        Returns:
            HTTP 200 Response with the user's profile JSON data.
        """

        user_profile = request.user.profile
        serializer = UserProfileSerializer(user_profile)
        return Response(serializer.data)

    def put(self, request):
        """Completely Updates the user profile.

        Arguments:
            request: the request data sent by the user, it is used
                     to get the user profile.

        Returns:
             HTTP 400 Response if the data is not valid with the errors,
             if not returns HTTP 200 Response with the update JSON data.
        """

        user_profile = request.user.profile
        serializer = UserProfileSerializer(user_profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        """Partially Updates the user profile.

        Arguments:
            request: the request data sent by the user, it is used
                     to get the user profile.

        Returns:
             HTTP 400 Response if the data is not valid with the errors,
             if not returns HTTP 200 Response with the update JSON data.
        """
        user_profile = request.user.profile
        serializer = UserProfileSerializer(user_profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        """Deletes the user profile.

            Arguments:
                request: the request data sent by the user, it is used
                         to get the user profile.

            Returns:
                returns HTTP 204 Response with no content.
        """
        user_profile = request.user.profile
        user_profile.user.delete()
        user_profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserAddressView(viewsets.ViewSet):
    """View for the user addresses.

    Lists, Creates, Updates and Deletes an Address, requires user authentication.
    """

    permission_classes = (IsAuthenticated, HasProfile)

    def list(self, request):
        """Lists all addresses the user has.

        Arguments:
            request: the request data sent by the user, it is used
                     to get the user profile.

        Returns:
            HTTP 200 Response with all addresses in
            the user's profile in JSON.
        """
        query_set = request.user.profile.addresses
        serializer = UserAddressSerializer(query_set, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Retrieves a certain address from the user's list

        Arguments:
            request: the request data sent by the user, it is used
                     to get the user profile.
            pk: the id of the address that the user want info about,
                it should by an integer.

        Returns:
            HTTP 404 Response if address is not found, if not,
            returns HTTP 200 Response with the address's JSON data.
        """
        address = get_object_or_404(UserAddressModel, sort=pk, user=request.user.profile)
        serializer = UserAddressSerializer(address)
        return Response(serializer.data)

    def create(self, request):
        """Creates a new address and adds it to the user's list.

        Arguments:
            request: the request data sent by the user, it is used
                     to get the user profile.

        Returns:
            HTTP 400 Response if the data is not valid, if not,
            returns HTTP 201 Response with the address's JSON data.
        """
        serializer = UserAddressSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user.profile)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        """Completely Updates a certain address from the user's list.

        Arguments:
            request: the request data sent by the user, it is used
                     to get the user profile.
            pk: the id of the address that the user wants to change,
                it should by an integer.

        Returns:
            HTTP 400 Response if the data is not valid with the errors,
            HTTP 404 Response if the address is not found
            if not returns HTTP 200 Response with the update JSON data.
        """
        address = get_object_or_404(UserAddressModel, sort=pk, user=request.user.profile)
        serializer = UserAddressSerializer(address, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        """Partially Updates a certain address from the user's list.

        Arguments:
            request: the request data sent by the user, it is used
                     to get the user profile.
            pk: the id of the address that the user wants to change,
                it should by an integer.

        Returns:
            HTTP 400 Response if the data is not valid with the errors,
            HTTP 404 Response if the address is not found
            if not returns HTTP 200 Response with the update JSON data.
        """
        address = get_object_or_404(UserAddressModel, sort=pk, user=request.user.profile)
        serializer = UserAddressSerializer(address, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """Deletes a certain address from the user's list.

            Arguments:
                request: the request data sent by the user, it is used
                         to get the user profile.
                pk: the id of the address that the user wants to delete,
                    it should by an integer.
            Returns:
                returns HTTP 204 Response with no content.
        """
        address = get_object_or_404(UserAddressModel, sort=pk, user=request.user.profile)
        address.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
