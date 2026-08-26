# from django.db.models import Q
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import status, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle, ScopedRateThrottle
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet
# from django.contrib.postgres.search import TrigramSimilarity
from django_filters.rest_framework import DjangoFilterBackend

from config.settings import CACHE_TTL
from notifications.models import Notifications
from tasks.models import Project, Task
from tasks.paginations import CustomPagination
from tasks.serializers import ProjectList, ProjectCreateAndUpdateSerializer, TaskListSerializer, \
    TaskCreateAndUpdateSerializer, BackgroundTaskSerializer
from celery.result import AsyncResult
from config.celery import app
from .tasks import add
from django.core.cache import cache


class BackgroundTaskViewSet(GenericViewSet):
    serializer_class = BackgroundTaskSerializer

    @action(detail=False, methods=['post'])
    def send_gmail(self, request):
        pass

    @action(detail=False, methods=['get'])
    def start_task(self, request):
        a = add.delay(1, 2)  # background ga yuborish!
        return Response({"task_id": a.id})

    # Natijani tekshirish
    @action(detail=False, methods=['post'], )
    def check_task(self, request):
        task_id = request.data['task_id']
        result = AsyncResult(task_id, app=app)

        if result.ready():  # Tayormi?
            return Response({"result": result.result})
        return Response({"status": "processing..."})


# Create your views here.
def salom(request):
    return JsonResponse({'message': 'Hello World!'})


class ProjectAPIView(APIView):
    throttle_scope = 'lists'
    throttle_classes = [ScopedRateThrottle]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'search',
                openapi.IN_QUERY,
                description="Qidirish so'zi",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                'page',
                openapi.IN_QUERY,
                description="Sahifa raqami",
                type=openapi.TYPE_INTEGER,
            ),
        ],
    )
        # project_list = []
        # for project in project:
        #     project_dict = {
        #         "id": project.id,
        #         "name": project.name,
        #         "description": project.description,
        #         "owner": project.owner.username,
        #     }
        #     project_list.append(project_dict)
        #
        # return JsonResponse(project_list, safe=False)

    @swagger_auto_schema(
        operation_summary="project yaratish",
        operation_description="Bu endpoint porject yasaydi",
        request_body=ProjectCreateAndUpdateSerializer,
        responses={
            201: openapi.Response(
                'Muvaffaqiyatli',
                ProjectCreateAndUpdateSerializer
            ),
            403: "Ruxsat yo'q",
        },
        tags=['task']
    )
    def post(self, request):
        # name = request.data.get('name')
        # description = request.data.get('description')
        # project = Project(name=name, description=description)
        # project.save()
        cache.delete('task_list')
        serializer = ProjectCreateAndUpdateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        project = get_object_or_404(Project, pk=pk)
        serializer = ProjectCreateAndUpdateSerializer(data=request.data, instance=project)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.data, status=status.HTTP_200_OK)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        project = get_object_or_404(Project, pk=pk)
        project.delete()
        return Response({'message': 'Success'})


# project/1/task/list/
# p = 1
# tasks = Task.objects.filter(project=p)
class ProjectDetailTaskAPIView(APIView):
    def get(self, request, pk=None):
        tasks = Task.objects.filter(project_id=pk)
        serializers = TaskListSerializer(tasks, many=True)
        return Response(serializers.data)


# class TaskAPIView(APIView):
#     def get(self, request):
#         tasks = Task.objects.all()
#         serializers = TaskListSerializer(tasks, many=True)
#         return Response(serializers.data)
#
#     def post(self, request):
#         serializers = TaskCreateAndUpdateSerializer(data=request.data)
#         serializers.is_valid(raise_exception=True)
#         serializers.save()
#         return Response(serializers.data, status=status.HTTP_201_CREATED)
#
#
# class TaskDetailAPIView(APIView):
#     def get(self, request, pk=None):
#         tasks = get_object_or_404(Task, pk=pk)
#         serializer = TaskListSerializer(tasks)
#         return Response(serializer.data)
#
#     def put(self, request, pk=None):
#         task = get_object_or_404(Task, pk=pk)
#         serializers = TaskCreateAndUpdateSerializer(instance=task, data=request.data)
#         serializers.is_valid(raise_exception=True)
#         serializers.save()
#         return Response(serializers.data, status=status.HTTP_200_OK)
#
#     def delete(self, request, pk=None):
#         task = get_object_or_404(Task, pk=pk)
#         task.delete()
#         return Response({'message': 'Success'})


class TaskModelViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskListSerializer

    # pagination_class = None

    filter_backends = [
        filters.SearchFilter,
        DjangoFilterBackend,
        filters.OrderingFilter
    ]

    search_fields = [
        'name',
        'description',
    ]

    filterset_fields = ["status", "to_user", "project"]
    ordering = ['created_time', 'id']
    permission_classes = [IsAuthenticated]

    # def get_queryset(self):
    #     search = self.request.query_params.get('search')
    #     if search:
    #         # return self.queryset.filter(Q(name__icontains=search) | Q(description__icontains=search))
    #         return self.queryset.annotate(similarity_name=TrigramSimilarity('name', search),
    #                                       similarity_desc=TrigramSimilarity('description', search)).filter(
    #             Q(similarity_name__gt=0.2) | Q(similarity_desc__gt=0.2)
    #         ).order_by('-similarity_name', '-similarity_desc')
    #     return self.queryset
    #

    def get_serializer_class(self):
        if self.action in ("create", "update"):
            return TaskCreateAndUpdateSerializer
        else:
            return TaskListSerializer

    @action(methods=['get'], detail=True)
    def project_into_task(self, request, pk=None):
        tasks = Task.objects.filter(project_id=pk)
        serializer = TaskListSerializer(tasks, many=True)
        return Response(serializer.data)

    @action(methods=['patch'], detail=True)
    def change(self, request, pk=None):
        task = get_object_or_404(Task, pk=pk)
        serializer = TaskCreateAndUpdateSerializer(instance=task, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    # def list(self, request):
    #     tasks = Task.objects.all()
    #     serializers = TaskListSerializer(tasks, many=True)
    #     return Response(serializers.data)
    #
    # def retrieve(self, request, pk=None):
    #     tasks = get_object_or_404(Task, pk=pk)
    #     serializer = TaskListSerializer(tasks)
    #     return Response(serializer.data)
    #
    # def create(self, request):
    #     serializers = TaskCreateAndUpdateSerializer(data=request.data)
    #     serializers.is_valid(raise_exception=True)
    #     serializers.save()
    #     return Response(serializers.data, status=status.HTTP_201_CREATED)
    #
    # def update(self, request, pk=None):
    #     task = get_object_or_404(Task, pk=pk)
    #     serializers = TaskCreateAndUpdateSerializer(instance=task, data=request.data)
    #     serializers.is_valid(raise_exception=True)
    #     serializers.save()
    #     return Response(serializers.data, status=status.HTTP_200_OK)
    #
    # def destroy(self, request, pk=None):
    #     task = get_object_or_404(Task, pk=pk)
    #     task.delete()
    #     return Response({'message': 'Success'})
