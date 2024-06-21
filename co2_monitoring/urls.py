"""
URL configuration for co2_monitoring project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
# from django.urls import path, include
# from sensor_data import views

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     #   path('', include('sensor_data.urls')),
#     path('data/', views.sensor_data_view, name='sensor_data'), 
# ]


from django.urls import path, include
from sensor_data import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('data/', views.save_sensor_data, name='save_sensor_data'),
    path('data1/', include('sensor_data1.urls')),
    path('api/', include('articles.urls')),
    path('apidonate/', include('donation.urls')),
    path('profile/', include('Profiles.urls')),
]
