from rest_framework.routers import SimpleRouter

from apps.products.views import ProductViewSet,CartReadView,CartProductView,CategoryViewSet,OrderViewSet

router = SimpleRouter()

router.register('products',ProductViewSet,basename='product')
router.register('carts',CartReadView,basename='cart')
router.register('cart_product',CartProductView,basename='cart_product')
router.register('category',CategoryViewSet,basename='category')
router.register('order',OrderViewSet,basename='order')

urlpatterns = []
urlpatterns += router.urls
