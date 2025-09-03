from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from inmunoterapia.models import Alergologia
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST
from django.http import HttpResponseBadRequest, HttpResponseForbidden, HttpResponseRedirect, JsonResponse
from django.utils.timezone import now
import traceback


@login_required
def inicio_alergologia(request):
    if not request.user.has_perm('inmunoterapia.ver_app_alergologia'):
        return render(request, "401.html", status=401)
    return render(request, 'main/index_inmu_aler.html')

@login_required
def filtro_alergologia(request):
    if not request.user.has_perm('inmunoterapia.ver_app_alergologia'):
        return render(request, "401.html", status=401)
    queryset = Alergologia.objects.exclude(CREADO__isnull=True)
    print("Parámentros GET recibidos:", request.GET)

    # FILTROS
    documento = request.GET.get('documento')
    sede = request.GET.get('sede')
    actividad = request.GET.get('actividad')
    resolucion_paciente = request.GET.get('resolucion_paciente')
    clasificacion = request.GET.get('clasificacion')
    mes = request.GET.get('mes')
    anio = request.GET.get('anio')
    diagnostico = request.GET.get('diagnostico')

    if documento:
        queryset = queryset.filter(DOCUMENTO__icontains=documento)
    if sede:
        queryset = queryset.filter(SEDE=sede)
    if clasificacion:
        queryset = queryset.filter(CLASIFICACION=clasificacion)
    if actividad:
        queryset = queryset.filter(ACTIVIDAD=actividad)
    if resolucion_paciente:
        queryset = queryset.filter(RESOLUCION_PACIENTE=resolucion_paciente)
    if anio:
        queryset = queryset.filter(AÑO_FOLIO=anio)
    if mes:
        queryset = queryset.filter(MES_FOLIO=mes)
    if diagnostico:
        queryset = queryset.filter(DIAGNOSTICO__icontains=diagnostico)
    
    page = request.GET.get('page', 1)
    paginator = Paginator(queryset, 100)
    try:
        pacientes_paginados = paginator.page(page)
    except PageNotAnInteger:
        pacientes_paginados = paginator.page(1)
    except EmptyPage:
        pacientes_paginados = paginator.page(paginator.num_pages)

    # Catálogos
    documento = (
        Alergologia.objects.exclude(DOCUMENTO__isnull=True).exclude(DOCUMENTO='')
        .values_list('DOCUMENTO', flat=True).distinct().order_by('DOCUMENTO')
    )
    sede = (
        Alergologia.objects.exclude(SEDE__isnull=True).exclude(SEDE='')
        .values_list('SEDE', flat=True).distinct().order_by('SEDE')
    )
    clasificacion = (
        Alergologia.objects.exclude(CLASIFICACION__isnull=True).exclude(CLASIFICACION='')
        .values_list('CLASIFICACION', flat=True).distinct().order_by('CLASIFICACION')
    )
    actividad = (
        Alergologia.objects.exclude(ACTIVIDAD__isnull=True).exclude(ACTIVIDAD='')
        .values_list('ACTIVIDAD', flat=True).distinct().order_by('ACTIVIDAD')
    )
    resolucion_paciente = (
        Alergologia.objects.exclude(RESOLUCION_PACIENTE__isnull=True).exclude(RESOLUCION_PACIENTE='')
        .values_list('RESOLUCION_PACIENTE', flat=True).distinct().order_by('RESOLUCION_PACIENTE')
    )
    anio = (
        Alergologia.objects.exclude(AÑO_FOLIO__isnull=True)
        .values_list('AÑO_FOLIO', flat=True).distinct().order_by('-AÑO_FOLIO')
    )

    # Diccionario de meses
    meses_nombres = {
        1: 'enero',
        2: 'febrero',
        3: 'marzo',
        4: 'abril',
        5: 'mayo',
        6: 'junio',
        7: 'julio',
        8: 'agosto',
        9: 'septiembre',
        10: 'octubre',
        11: 'noviembre',
        12: 'diciembre',
    }
    meses_nombres_inverso = {v.lower(): k for k, v in meses_nombres.items()}

    # Obtener todos los valores distintos y ordenarlos en Python
    mes_raw = (
        Alergologia.objects
        .exclude(MES_FOLIO__isnull=True)
        .exclude(MES_FOLIO='')
        .values_list('MES_FOLIO', flat=True)
        .distinct()
    )

    # Ordenar por número de mes, detectando si es texto o número
    mes = sorted(
        mes_raw,
        key=lambda x: meses_nombres_inverso.get(str(x).strip().lower(),
                                                int(x) if str(x).isdigit() else 99),
        reverse=True
    )

    diagnostico = (
        Alergologia.objects.exclude(DIAGNOSTICO__isnull=True).exclude(DIAGNOSTICO='')
        .values_list('DIAGNOSTICO', flat=True).distinct().order_by('DIAGNOSTICO')
    )

    context = {
        'pacientes': pacientes_paginados,
        'documento': documento,
        'sede': sede,
        'clasificacion': clasificacion,
        'actividad': actividad,
        'resolucion_paciente': resolucion_paciente,
        'anio': anio,
        'mes': mes,
        'meses_nombres': meses_nombres,
        'diagnostico': diagnostico,
    }
    return render(request, 'alergologia/index_alergologia.html', context)

@login_required
def historial_alergologia(request, ID_SHARE):
    if not request.user.has_perm('inmunoterapia.ver_app_alergologia'):
        return render(request, "401.html", status=401)
    try:
        historial = Alergologia.objects.filter(ID_SHARE=ID_SHARE).order_by('-FECHA_FOLIO')
        if not historial:
            return JsonResponse({'success': False, 'message': 'No se encontró el historial.'}, status=404)
        print("📩 ID_SHARE recibido:", ID_SHARE)
        print("📋 Historial encontrado:", historial.count())

        html = render_to_string('alergologia/historial_alergologia.html', {'historial': historial}, request=request)
        return JsonResponse({'success': True, 'html': html})
    except Exception as e:
        print("⚠️ Error al obtener el historial:", str(e))
        return JsonResponse({'success': False, 'message': 'Error interno del servidor.'}, status=500)
    

@login_required
def cargar_edicion_alergologia(request, idshare):
    if not request.user.has_perm('inmunoterapia.editar_alergologia'):
        return HttpResponseForbidden("No tienes permiso para cambiar estado.")

    paciente = get_object_or_404(Alergologia, ID_SHARE=idshare)

    resolucion_paciente = Alergologia.objects.exclude(RESOLUCION_PACIENTE__isnull=True)\
    .exclude(RESOLUCION_PACIENTE='')\
    .values_list('RESOLUCION_PACIENTE', flat=True).distinct().order_by('-RESOLUCION_PACIENTE')

    html = render_to_string(
        "alergologia/editar_alergologia.html",
        {"paciente":paciente, "resolucion_paciente": resolucion_paciente},
        request=request
    )
    return JsonResponse({"success":True, "html": html})

@login_required
@require_POST
def guardar_edicion_alergologia(request, idshare):
    try:
        paciente = get_object_or_404(Alergologia, ID_SHARE=idshare)

        paciente.RESOLUCION_PACIENTE = request.POST.get("resolucion_paciente") or None
        paciente.OBSERVACIONES_GENERALES = request.POST.get("observaciones") or None

        val = (paciente.RESOLUCION_PACIENTE or "").strip().lower()
        clasificacion = "No clasificado"
        if val in [
            "pendiente inicio inmunoterapia",
            "paciente remitido con otra entidad",
            "inicio de biológico",
            "escalonamiento a junta médica",
            "entrenamiento con inmunoterapia",
            "en espera de resultado de pruebas",
            "en espera de mejoría por tratamiento farmacológico",
            "en espera de control con el alergólogo",
            "alta del paciente"
        ]:
            clasificacion = "Clasificado"

        paciente.CLASIFICACION = clasificacion
        paciente.save(update_fields=[
            "RESOLUCION_PACIENTE", "OBSERVACIONES_GENERALES", "CLASIFICACION"
        ])

        return JsonResponse({
            "success": True,
            "resolucion": paciente.RESOLUCION_PACIENTE,
            "clasificacion": paciente.CLASIFICACION,
            "id": paciente.ID_SHARE
        })

    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=400)

@login_required
def cargar_agregar_alergologia(request, idshare):
    if not request.user.has_perm('inmunoterapia.agregar_alergologia'):
        return HttpResponseForbidden("No tienes permiso para cambiar estado.")

    paciente = get_object_or_404(Alergologia, ID_SHARE=idshare)

    resolucion_paciente = Alergologia.objects.exclude(RESOLUCION_PACIENTE__isnull=True)\
    .exclude(RESOLUCION_PACIENTE='')\
    .values_list('RESOLUCION_PACIENTE', flat=True).distinct().order_by('-RESOLUCION_PACIENTE')

    html = render_to_string(
        "alergologia/agregar_alergologia.html",
        {"paciente":paciente, "resolucion_paciente": resolucion_paciente},
        request=request
    )
    return JsonResponse({"success":True, "html": html})


@login_required
@require_POST
def guardar_agregar_alergologia(request, idshare):
    try:
        paciente = get_object_or_404(Alergologia, ID_SHARE=idshare)

        paciente.RESOLUCION_PACIENTE = request.POST.get("resolucion_paciente") or None
        paciente.OBSERVACIONES_GENERALES = request.POST.get("observaciones") or None

        # calcular clasificación en base a resolución
        val = (paciente.RESOLUCION_PACIENTE or "").strip().lower()
        clasificacion = "No clasificado"
        if val in [
            "pendiente inicio inmunoterapia",
            "paciente remitido con otra entidad",
            "inicio de biológico",
            "escalonamiento a junta médica",
            "entrenamiento con inmunoterapia",
            "en espera de resultado de pruebas",
            "en espera de mejoría por tratamiento farmacológico",
            "en espera de control con el alergólogo",
            "alta del paciente"
        ]:
            clasificacion = "Clasificado"

        paciente.CLASIFICACION = clasificacion
        paciente.MODIFICADO = now()
        paciente.USUARIO_INVITADO = request.user.username if request.user.is_authenticated else "Sistema"

        paciente.save(update_fields=[
            "RESOLUCION_PACIENTE", "OBSERVACIONES_GENERALES",
            "CLASIFICACION", "MODIFICADO", "USUARIO_INVITADO"
        ])

        return JsonResponse({
            "success": True,
            "resolucion": paciente.RESOLUCION_PACIENTE,
            "clasificacion": paciente.CLASIFICACION,
            "usuario": paciente.USUARIO_INVITADO,
            "fecha": paciente.MODIFICADO.strftime("%Y-%m-%d") if paciente.MODIFICADO else "",
            "id": paciente.ID_SHARE
        })

    except Exception as e:
        print(traceback.format_exc())
        return HttpResponseBadRequest(f"Error al guardar: {str(e)}")