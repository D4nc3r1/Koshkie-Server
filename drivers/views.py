#  Copyright (c) Code Written and Tested by Ahmed Emad in 04/01/2020, 12:48
from django.contrib.auth import login
from rest_framework import viewsets, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from drivers.models import DriverProfileModel, DriverReviewModel
from drivers.permissions import DriverProfilePermissions, DriverReviewPermissions
from drivers.serializers import DriverProfileSerializer, DriverReviewSerializer


class DriverProfileView(viewsets.ViewSet):
    permission_classes = (DriverProfilePermissions,)

    def list(self, request):
        try:
            user_longitude = float(request.GET.get('longitude'))
            user_latitude = float(request.GET.get('latitude'))
        except Exception:
            return Response("invalid coordinates", status=status.HTTP_400_BAD_REQUEST)

        # min_active_time = timezone.now() - timezone.timedelta(seconds=10)
        # available_drivers = DriverProfileModel.objects.filter(is_active=True, is_busy=False,
        #                                                       last_time_online__gte=min_active_time)
        query = """SELECT id, (6367*acos(cos(radians(%2f))
                      *cos(radians(live_location_longitude))*cos(radians(live_location_latitude)-radians(%2f))
                      +sin(radians(%2f))*sin(radians(live_location_latitude))))
                      AS distance FROM drivers_driverprofilemodel WHERE
                      distance < %2f ORDER BY distance LIMIT 0, %d""" % (
            float(user_latitude),
            float(user_longitude),
            float(user_latitude),
            2.5,
            10
        )

        queryset = DriverProfileModel.objects.raw(query)

        serializer = DriverProfileSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, username=None):
        driver_profile = get_object_or_404(DriverProfileModel, account__username=username)
        serializer = DriverProfileSerializer(driver_profile)
        return Response(serializer.data)

    def create(self, request):
        if not request.user.is_authenticated:
            serializer = DriverProfileSerializer(data=request.data)
            if serializer.is_valid():
                driver_profile = serializer.save()
                login(request, driver_profile.account)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    def update(self, request, username=None):
        driver_profile = get_object_or_404(DriverProfileModel, account__username=username)
        self.check_object_permissions(request, driver_profile)
        serializer = DriverProfileSerializer(driver_profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, username=None):
        driver_profile = get_object_or_404(DriverProfileModel, account__username=username)
        self.check_object_permissions(request, driver_profile)
        serializer = DriverProfileSerializer(driver_profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, username=None):
        driver_profile = get_object_or_404(DriverProfileModel, account__username=username)
        self.check_object_permissions(request, driver_profile)
        driver_profile.account.delete()
        driver_profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DriverReviewView(viewsets.ViewSet):
    permission_classes = (DriverReviewPermissions,)

    def list(self, request, username=None):
        query_set = DriverProfileModel.objects.filter(account__username=username).get().reviews.all()
        serializer = DriverReviewSerializer(query_set, many=True)
        return Response(serializer.data)

    def retrieve(self, request, username=None, pk=None):
        review = get_object_or_404(DriverReviewModel, driver__account__username=username, sort=pk)
        serializer = DriverReviewSerializer(review)
        return Response(serializer.data)

    def create(self, request, username=None):
        serializer = DriverReviewSerializer(data=request.data)
        if serializer.is_valid():
            driver = get_object_or_404(DriverProfileModel, account__username=username)
            serializer.save(user=request.user.profile, driver=driver)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, username=None, pk=None):
        review = get_object_or_404(DriverReviewModel, driver__account__username=username, sort=pk)
        self.check_object_permissions(request, review)
        serializer = DriverReviewSerializer(review, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, username=None, pk=None):
        review = get_object_or_404(DriverReviewModel, driver__account__username=username, sort=pk)
        self.check_object_permissions(request, review)
        serializer = DriverReviewSerializer(review, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, username=None, pk=None):
        review = get_object_or_404(DriverReviewModel, driver__account__username=username, sort=pk)
        self.check_object_permissions(request, review)
        driver = review.driver
        review.delete()

        driver.calculate_rating()
        driver.resort_reviews(review.sort)
        driver.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
