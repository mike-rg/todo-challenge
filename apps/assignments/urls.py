from rest_framework.routers import DefaultRouter

from .views import AssignmentsViewSet


app_name = 'assignments'

route = DefaultRouter()
route.register(r'assignments', AssignmentsViewSet, basename='assignments')
urlpatterns = route.urls
