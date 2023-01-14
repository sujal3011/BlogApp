from django.urls import path,include

urlpatterns = [
   
    path('account/', include('user_profile.urls')),
    path('blog/', include('blog.urls')),
]
