from django.contrib import admin
from .models import Inmunoterapia, Alergologia

@admin.register(Inmunoterapia)
class InmunoterapiaAdmin(admin.ModelAdmin):
    list_display = (
        'DOCUMENTO',
        'NOMBRE_PACIENTE',
        'SEDE',
        'CLASIFICACION_TRATAMIENTO',
        'NO_ADHERENCIA',
        'FINALIZACION_TRATAMIENTO',
        'CREADO',
    )

    # Filtros que quieres mostrar en la parte derecha del admin
    list_filter = (
        'SEDE',
        'CLASIFICACION_TRATAMIENTO',
        'NO_ADHERENCIA',
        'FINALIZACION_TRATAMIENTO',
        ('CREADO', admin.DateFieldListFilter),
        ('MODIFICADO', admin.DateFieldListFilter),
    )

    search_fields = ('DOCUMENTO', 'NOMBRE_PACIENTE')  # Para búsquedas rápidas

    def has_module_permission(self, request):
        return request.user.is_superuser

@admin.register(Alergologia)
class AlergologiaAdmin(admin.ModelAdmin):
    list_display = (
        'DOCUMENTO',
        'USUARIO_INVITADO',
        'SEDE',
        'CLASIFICACION',
        'INMUNOTERAPIA',
        'ACTIVIDAD',
        'CREADO',
    )

    list_filter = (
        'SEDE',
        'CLASIFICACION',
        'INMUNOTERAPIA',
        'ACTIVIDAD',
        ('CREADO', admin.DateFieldListFilter),
        ('MODIFICADO', admin.DateFieldListFilter),
    )

    search_fields = ('DOCUMENTO', 'USUARIO_INVITADO')

    def has_module_permission(self, request):
        return request.user.is_superuser
