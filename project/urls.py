from django.contrib import admin
from django.urls import include, path
from tickets import views
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter()
router.register('guests', views.viewsets_guest)
router.register('movies', views.viewsets_movie)
router.register('reservations', views.viewsets_reservation)

urlpatterns = [
    path('admin/', admin.site.urls),

    #1
    path('django/jsonresponsenomodel/', views.no_rest_no_model),
    #2
    path('django/jsonresponsewithmodel/', views.from_model),
    #3 GET POST from rest framework
    path('rest/fbvlist/', views.FBV_List),
    #3 GET PUT DELETE
    path('rest/fbvlist/<int:pk>', views.FBV_pk),
    #4 GET POST from rest framework CBV
    path('rest/cbv/', views.CBV_list.as_view()),
    #4 GET PUT DELETE
    path('rest/cbv/<int:pk>', views.CBV_pk.as_view()),
    
    #5 GET POST from rest framework CBV mixins
    path('rest/mixins/', views.mixins_list.as_view()),
    #5 GET PUT DELETE mixins
    path('rest/mixins/<int:pk>', views.mixins_pk.as_view()),
    #6 GET POST from rest framework CBV generics
    path('rest/generics/', views.generics_list.as_view()),
    #6 GET PUT DELETE generics
    path('rest/generics/<int:pk>', views.generics_pk.as_view()),

    #viewsets
    path('rest/viewsets/', include(router.urls)),

    #find movie FBV
    path('fbv/findmovie', views.find_movie),

    #reservations FBV
    path('fbv/newreservation', views.new_reservation),


    #rest auth url
    path('api-auth', include('rest_framework.urls')),

    #token authentication
    path('api-token-auth', obtain_auth_token),

    #post pk generics
    #path('post/generics', views.Post_list.as_view()),
    path('post/generics/<int:pk>', views.Post_pk.as_view()),

]
