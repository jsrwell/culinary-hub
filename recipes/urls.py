from django.urls import path
from recipes.views import my_view1, my_view2, my_view3


urlpatterns = [
    path('', my_view1),
    path('sobre/', my_view2),
    path('contato/', my_view3)
]
