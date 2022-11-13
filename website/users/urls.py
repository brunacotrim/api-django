from rest_framework.routers import SimpleRouter

from .views import UserViewSet


router_users = SimpleRouter()
router_users.register('users', UserViewSet)

urlpatterns = [

]