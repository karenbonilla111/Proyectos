from django.urls import path
from . import views

app_name='inmunoterapia'

urlpatterns = [
    path('', views.inicio_inmunoterapia, name='inicio_inmunoterapia'),
    path('lista/', views.lista_inmunoterapia, name='lista_inmunoterapia'),
    path('alergologia/', views.inicio_alergologia, name='inicio_alergologia'),
    path('historico/<str:IDSHARE>/', views.historico_inmunoterapia, name='historico_inmunoterapia'),
    path('filtro-alergologias/', views.filtro_alergologia, name='filtro_alergologia'),
    path('historial_alergologia/<str:ID_SHARE>/', views.historial_alergologia, name='historial_alergologia'),
    path("cargar-edicion/<str:idshare>/", views.cargar_edicion_inmunoterapia, name="cargar_edicion"),
    path("guardar-edicion/<str:idshare>/", views.guardar_edicion_inmunoterapia, name="guardar_edicion"),
    path("cargar-edicion-alergologia/<int:idshare>/", views.cargar_edicion_alergologia, name="cargar_edicion_alergologia"),
    path("guardar-edicion-alergologia/<int:idshare>/", views.guardar_edicion_alergologia, name="guardar_edicion_alergologia"),
    path("cargar-agregar/<int:idshare>/", views.cargar_agregar_inmunoterapia, name="cargar_agregar_inmunoterapia"),
    path("guardar-agregar-inmunoterapia/<int:idshare>/", views.guardar_agregar_inmunoterapia, name="guardar_agregar_inmunoterapia"),
    path("cargar-agregar-alergologia/<int:idshare>/", views.cargar_agregar_alergologia, name="cargar_agregar_alergologia"),
    path("guardar-agregar-alergologia/<int:idshare>/", views.guardar_agregar_alergologia, name="guardar_agregar_alergologia"),
]