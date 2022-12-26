from rest_framework.routers import SimpleRouter

from .views import ProductViewSet, VariationViewSet


router_products = SimpleRouter()
router_products.register('products', ProductViewSet)
router_products.register('variations', VariationViewSet)

urlpatterns = [

]