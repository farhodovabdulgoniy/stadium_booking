from . utils import nearby_filter
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from accounts.models import CustomUser
from accounts.serializers import CustomUserSerializer
from datetime import datetime
from django.utils.timezone import make_aware
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .permissions import (
    IsAdmin,
    IsOwnerOrAdmin,
    IsUserOrAdmin,
)
from .models import (
    Stadium,
    Book,
    TaskOrder,
)
from .serializers import (
    StadiumSerializer,
    BookSerializer,
)


class StadiumView(APIView):
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def get(self, request):
        queryset = Stadium.objects.filter(owner__id=request.user.id)
        serializer = StadiumSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        request.data['owner'] = request.user.id
        serializer = StadiumSerializer(data=request.data, many=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class StadiumDetailView(APIView):
    def get(self, request, pk):
        queryset = get_object_or_404(Stadium, id=pk)
        serializer = StadiumSerializer(queryset, many=False)
        return Response(serializer.data)


class StadiumUpdateView(APIView):
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def patch(self, request, pk):
        queryset = get_object_or_404(Stadium, id=pk)
        serializer = StadiumSerializer(
            instance=queryset, data=request.data, many=False, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        queryset = get_object_or_404(Stadium, id=pk)
        queryset.delete()
        return Response({
            'message': 'Stadium deleted successfully!'
        }, status=204)


class StadiumsFilter(APIView):
    def get(self, request):
        # Get user location from frontend, for example (40.1053871882837,   )
        user_latitude = request.query_params.get('user_latitude', 0)
        user_longitude = request.query_params.get('user_longitude', 0)

        time_from = request.query_params.get('time_from', 0)
        time_to = request.query_params.get('time_to', 0)

        # if user wants to filter by time
        if time_from and time_to:
            time_from = datetime.strptime(time_from, '%Y-%m-%d %H:%M')
            time_to = datetime.strptime(time_to, '%Y-%m-%d %H:%M')
            queryset = Stadium.objects.exclude(
                (Q(book__busy_from__lte=time_to)
                & Q(book__busy_to__gte=time_from))
            )
        else:
            queryset = Stadium.objects.all()
        return Response(nearby_filter(user_latitude, user_longitude, queryset))


class BookView(APIView):
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def get(self, request):
        queryset = Book.objects.filter(stadium__owner__id=request.user.id)
        serializer = BookSerializer(queryset, many=True)
        return Response(serializer.data)


class BookCancelView(APIView):
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def get(self, request, pk):
        queryset = get_object_or_404(Book, id=pk)
        if queryset.status == 'Pending':
            queryset.status = 'Canceled'
            queryset.is_busy = False
            queryset.save()
            return Response({
                'message': 'Book canceled successfully!'
            }, status=200)

        return Response({
            'error': 'Invalid status.'
        }, status=400)


class BookCreateView(APIView):
    permission_classes = [IsAuthenticated, IsUserOrAdmin]

    def post(self, request):
        request.data['user'] = request.user.id
        serializer = BookSerializer(data=request.data, many=False)

        if Book.objects.filter(
            Q(busy_from__lte=datetime.strptime(request.data.get('busy_from'), '%Y-%m-%d %H:%M:%S'))
            & Q(busy_to__gte=datetime.strptime(request.data.get('busy_to'), '%Y-%m-%d %H:%M:%S'))
            & Q(stadium__id=int(request.data['stadium']))
        ).exists():
            return Response({
                'error': 'The stadium is occupied in the current interval.',
            }, status=400)

        if serializer.is_valid():
            serializer.save()

            time_now = datetime.now()
            target = datetime.strptime(request.data.get('busy_to'), '%Y-%m-%d %H:%M:%S')

            diff = target - time_now
            schedule, created = IntervalSchedule.objects.get_or_create(
                every=diff.seconds,
                period=IntervalSchedule.SECONDS
            )
            task = PeriodicTask.objects.create(
                interval=schedule,
                name='Time Checker',
                task='stadium_app.tasks.time_checker',
            )
            TaskOrder.objects.create(
                book=Book.objects.get(id=serializer.data['id']),
                periodic_task=task,
            )

            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)


##################################### Only Admin features ###########################################

class FilterStadiumsByOwner(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request, pk):
        queryset = Stadium.objects.filter(owner__id=pk)
        serializer = StadiumSerializer(queryset, many=True)
        return Response(serializer.data)


class OwnerListView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        queryset = CustomUser.objects.filter(role='Owner')
        serializer = CustomUserSerializer(queryset, many=True)
        return Response(serializer.data)


class UserListView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        queryset = CustomUser.objects.filter(role='User')
        serializer = CustomUserSerializer(queryset, many=True)
        return Response(serializer.data)


class OwnerDetailView(APIView):
    parser_classes = [IsAuthenticated, IsAdmin]

    def get(self, request, pk):
        queryset = get_object_or_404(CustomUser, id=pk, role='Owner')
        serializer = CustomUserSerializer(queryset, many=False)
        return Response(serializer.data)


class UserDetailView(APIView):
    parser_classes = [IsAuthenticated, IsAdmin]

    def get(self, request, pk):
        queryset = get_object_or_404(CustomUser, id=pk, role='User')
        serializer = CustomUserSerializer(queryset, many=False)
        return Response(serializer.data)
