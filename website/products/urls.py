from rest_framework.routers import SimpleRouter

from .views import ProductViewSet


router_products = SimpleRouter()
router_products.register('products', ProductViewSet)

urlpatterns = [

]