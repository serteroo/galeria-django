from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from core import views as v
from django.contrib.auth import views as auth_views
from core import views




urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),

    # Páginas
    path('', v.login_page, name='login_page'),
    path('dashboard/', v.dashboard_empleado, name='dash_empleado'),
    path('dashboard-admin/', v.dashboard_admin, name='dash_admin'),

    # Empleado
    path('dashboard/horarios/', v.horario_page, name='horarios'),
    path('dashboard/liquidaciones/', v.liquidaciones_list, name='liquidaciones'),
    path('dashboard/contrato/', v.contrato_empleado_page, name='contrato_empleado'),

    # Admin
    path('dashboard-admin/horarios/', v.horario_admin_page, name='horarios_admin'),
    path("dashboard-admin/empleados/crear/", views.empleado_crear, name="empleado_crear"),
    path('dashboard-admin/liquidaciones/', v.liquidaciones_list, name='liquidaciones_admin'),
    path('dashboard-admin/contratos/', v.contratos_admin_page, name='contratos_admin'),
    path('dashboard-admin/contratos/nuevo/', v.contrato_create, name='contrato_create'),
    path('dashboard-admin/contratos/<int:pk>/editar/', v.contrato_edit, name='contrato_edit'),
    path('dashboard-admin/contratos/<int:pk>/eliminar/', v.contrato_delete, name='contrato_delete'),

    # Gestión de cargos
    path('dashboard-admin/empleados/cargo/<int:pk>/', v.empleado_cargo_edit, name='empleado_cargo_edit'),
    path("dashboard-admin/crud-cargo/", v.gestion_cargos, name="crud_cargo"),
    path("dashboard-admin/crud-cargo/nuevo/", v.cargo_create, name="cargo_create"),
    path("dashboard-admin/crud-cargo/<int:pk>/editar/", v.cargo_edit, name="cargo_edit"),
    path("dashboard-admin/crud-cargo/<int:pk>/eliminar/", v.cargo_delete, name="cargo_delete"),
    
    # API
    path('api/login/', v.login_json, name='login_json'),
    path('api/logout/', v.logout_view, name='logout'),
    path('api/me/', v.me, name='me'),
   
     # Zonas de trabajo (CRUD)
    path('dashboard-admin/zonas/', v.zonas_list, name='zonas_list'),
    path('dashboard-admin/zonas/nueva/', v.zona_create, name='zona_create'),
    path('dashboard-admin/zonas/<int:pk>/editar/', v.zona_edit, name='zona_edit'),
    path('dashboard-admin/zonas/<int:pk>/eliminar/', v.zona_delete, name='zona_delete'),
    

# CRUD Turno-Jornada
    path('dashboard-admin/horarios/jornada/', v.horario_jornada, name='horario_jornada'),
    path('dashboard-admin/horarios/jornada/nuevo/', v.horario_create, name='horario_create'),
    path('dashboard-admin/horarios/jornada/<int:pk>/editar/', v.horario_update, name='horario_update'),
    path('dashboard-admin/horarios/jornada/<int:pk>/eliminar/', v.horario_delete, name='horario_delete'),



    # Asignación de zona a empleados
    path('dashboard-admin/empleados/zonas/', v.empleado_zonas_list, name='empleado_zonas_list'),
    path('dashboard-admin/empleados/<int:pk>/zona/', v.empleado_zona_edit, name='empleado_zona_edit'),
] + (static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) if settings.DEBUG else [])