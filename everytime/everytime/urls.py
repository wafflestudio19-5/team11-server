"""team11 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path
from . import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('user.urls')),
    path('api/v1/', include('emailcode.urls')),
    path('api/v1/', include('university.urls')),
    path('api/v1/', include('department.urls')),
    path('api/v1/', include('board.urls')),
    path('api/v1/', include('article.urls')),
    path('api/v1/', include('comment.urls')),
    path('api/v1/', include('message.urls')),
    path('api/v1/', include('lecture.urls')),
    path('api/v1/', include('review.urls')),
    path('api/v1/', include('information.urls')),
    path('api/v1/', include('schedule.urls')),
    path('api/v1/', include('customlecture.urls'))
]

urlpatterns +=[path('api-auth/', include('rest_framework.urls')), ]

if settings.DEBUG_TOOLBAR:
    import debug_toolbar
    urlpatterns += [
        path(r'__debug__/', include(debug_toolbar.urls)),
    ]
