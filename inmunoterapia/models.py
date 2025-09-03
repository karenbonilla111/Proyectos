from django.db import models

class Inmunoterapia(models.Model):
    IDSHARE = models.AutoField(primary_key=True)
    EPS = models.CharField(max_length=200, null=True, blank=True) # <-- Clave única para relacionar
    SEDE = models.CharField(max_length=6, null=True, blank=True)
    DOCUMENTO = models.CharField(max_length=100, null=True, blank=True)
    NOMBRE_PACIENTE = models.CharField(max_length=100, null=True, blank=True)
    EDAD = models.IntegerField(null=True, blank=True)
    TELEFONO = models.CharField(max_length=100, null=True, blank=True)
    HC_MEDICAMENTO = models.CharField(max_length=10000, null=True, blank=True)
    FECHA_ULTIMA_VACUNA= models.DateTimeField(null=True, blank=True)
    DOSIS = models.FloatField(null=True, blank=True)
    NUMERO_DOSIS_APLICADA = models.IntegerField(null=True, blank=True)
    ESCALA_VISUAL_ANALOGA_MEJORIA = models.CharField(max_length=200, null=True, blank=True)
    REGISTRO_ADHERENCIA = models.CharField(max_length=300, null=True, blank=True)
    NO_ADHERENCIA = models.CharField(max_length=300, null=True, blank=True)
    OTROS = models.CharField(max_length=1000, null=True, blank=True)
    MEDICO_TRATANTE = models.CharField(max_length=200, null=True, blank=True)
    AUXILIAR_RESPONSABLE = models.CharField(max_length=200, null=True, blank=True)
    FECHA_PROXIMA_CITA = models.DateTimeField(null=True, blank=True)
    FINALIZACION_TRATAMIENTO = models.CharField(max_length=100)
    CREADO = models.DateTimeField(null=True, blank=True)
    CREADO_POR = models.CharField(max_length=200, null=True, blank=True)
    MODIFICADO = models.DateTimeField(null=True, blank=True)
    MODIFICADO_POR = models.CharField(max_length=200, null=True, blank=True)
    FECHA_ULTIMO_FOLIO = models.DateTimeField(null=True, blank=True)
    ID_SQL = models.IntegerField(null=True, blank=True)
    CLASIFICACION_TRATAMIENTO = models.CharField(max_length=200, null=True, blank=True)
    class Meta:
        db_table = 'SA_PacientesInmunoterapia'
        managed = False
        permissions = [("ver_app_inmunoterapia", "Puede ver la aplicación de inmunoterapia"),
                       ("editar_inmunoterapia", "Puede editar registros de inmunoterapia"),
                       ("agregar_inmunoterapia", "Puede agregar registros de inmunoterapia"),]

class Alergologia(models.Model):
    ID_SHARE = models.AutoField(primary_key=True)
    FOLIO = models.CharField(max_length=100, null=True, blank=True)
    FECHA_FOLIO = models.DateField(null=True, blank=True)
    MES_FOLIO = models.CharField(max_length=100, null=True, blank=True)
    AÑO_FOLIO = models.IntegerField(null=True, blank=True)
    DOCUMENTO = models.CharField(max_length=100, null=True, blank=True)
    SEDE = models.CharField(max_length=6, null=True, blank=True)
    ACTIVIDAD = models.CharField(max_length=200, null=True, blank=True)
    CODIGO_DIGNOSTICO = models.CharField(max_length=100, null=True, blank=True)
    DIAGNOSTICO = models.CharField(max_length=200, null=True, blank=True)
    PRUEBA_PROVOCACION_MEDICAMENTO = models.CharField(max_length=200, null=True, blank=True)
    PRUEBA_PROVOCACION_ALIMENTO = models.CharField(max_length=200, null=True, blank=True)
    PRUEBA_PRICK = models.CharField(max_length=200, null=True, blank=True)
    PRUEBA_PARCHE_ALIMENTOS_MEDICAMENTOS = models.CharField(max_length=200, null=True, blank=True)
    PRUEBA_ALIMENTOS_MENORES_A_2_AÑOS = models.CharField(max_length=200, null=True, blank=True)
    PRUEBA_PARCHE_BATERIA_ESTANDAR = models.CharField(max_length=200, null=True, blank=True)
    PRUEBA_CUTANEA_AEROALERGENOS = models.CharField(max_length=200, null=True, blank=True)
    PRUEBA_CUTANEA_ALIMENTOS = models.CharField(max_length=200, null=True, blank=True)
    TRATAMIENTO_FARMACOLOGICO = models.CharField(max_length=200, null=True, blank=True)
    INMUNOTERAPIA = models.CharField(max_length=200, null=True, blank=True)
    FECHA_ULTIMA_INMUNOTERAPIA = models.DateField(null=True, blank=True)
    RESOLUCION_PACIENTE = models.CharField(max_length=200, null=True, blank=True)
    OBSERVACIONES_GENERALES = models.CharField(max_length=1000, null=True, blank=True, db_column='OBSERVACIONES_GENERALES_')
    CLASIFICACION = models.CharField(max_length=200, null=True, blank=True)
    USUARIO_INVITADO = models.CharField(max_length=200, null=True, blank=True)
    CREADO = models.DateField(null=True, blank=True)
    CREADO_POR = models.CharField(max_length=200, null=True, blank=True)
    MODIFICADO = models.DateField(null=True, blank=True)
    MODIFICADO_POR = models.CharField(max_length=200, null=True, blank=True)
    MEDICAMENTOS_INMUNOTERAPIA = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        db_table = 'SA_PacientesInmunoterapia_Alergologia'
        managed = False
        permissions = [("ver_app_alergologia", "Puede ver la aplicación de alergología"),
                       ("editar_alergologia", "Puede editar registros de alergología"),
                       ("agregar_alergologia", "Puede agregar registros de alergología"),]