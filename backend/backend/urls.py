"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from reagents import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'pictograms', views.PictogramViewSet)
router.register(r'clp-classifications', views.ClpClassificationViewSet)
router.register(r'hazard-statements', views.HazardStatementViewSet)
router.register(r'precautionary-statements', views.PrecautionaryStatementViewSet)
router.register(r'reagent-types', views.ReagentTypeViewSet)
router.register(r'producers', views.ProducerViewSet)
router.register(r'concentrations', views.ConcentrationViewSet)
router.register(r'units', views.UnitViewSet)
router.register(r'purities-qualities', views.PurityQualityViewSet)
router.register(r'storage-conditions', views.StorageConditionViewSet)
router.register(r'safety-data-sheets', views.SafetyDataSheetViewSet)
router.register(r'safety-instructions', views.SafetyInstructionViewSet)
router.register(r'reagents', views.ReagentViewSet)
router.register(r'projects-procedures', views.ProjectProcedureViewSet)
router.register(r'laboratories', views.LaboratoryViewSet)
router.register(r'personal-reagents', views.PersonalReagentViewSet, basename="personal_reagents")
router.register(r'notifications', views.NotificationViewSet, basename="notifications")
router.register(r'reagent-requests', views.ReagentRequestViewSet)

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
    path('user-manual/', views.UserManualView.as_view(), name='user_manual'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += [
        path('admin/', admin.site.urls),
        path('__debug__/', include('debug_toolbar.urls')),
        path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    ]
