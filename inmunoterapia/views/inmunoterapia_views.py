import traceback
from django.http import HttpResponseBadRequest, HttpResponseForbidden, JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from inmunoterapia.models import Inmunoterapia
from django.db.models.functions import ExtractMonth, ExtractYear, Upper
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.http import require_POST
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404, render
from django.utils.dateparse import parse_date
from django.utils.timezone import now
from django.utils import timezone
from datetime import datetime

@login_required
def inicio_inmunoterapia(request):
    if not request.user.has_perm('inmunoterapia.ver_app_inmunoterapia'):
        return render(request, "401.html", status=401)
    return render(request, 'main/index_inmu_aler.html')

@login_required
def lista_inmunoterapia(request):
    if not request.user.has_perm('inmunoterapia.ver_app_inmunoterapia'):
        return render(request, "401.html", status=401)
    queryset = Inmunoterapia.objects.exclude(CREADO__isnull=True)
    print("Parámetros GET recibidos:", request.GET)


    # Filtros GET
    documento = request.GET.get('documento')
    sede = request.GET.get('sede')
    clasificacion = request.GET.get('clasificacion')
    no_adherencia = request.GET.get('no_adherencia')
    adherente = request.GET.get('paciente_adherente')
    finalizacion = request.GET.get('finalizacion')
    anio = request.GET.get('anio')
    mes = request.GET.get('mes')
    print("Año GET:", anio)
    print("Mes GET:", mes)

    # Aplicar filtros
    if documento:
        queryset = queryset.filter(DOCUMENTO__icontains=documento)
    if sede:
        queryset = queryset.filter(SEDE=sede)
    if clasificacion:
        queryset = queryset.filter(CLASIFICACION_TRATAMIENTO=clasificacion)
    if finalizacion:
        queryset = queryset.filter(FINALIZACION_TRATAMIENTO=finalizacion)
    if no_adherencia:
        queryset = queryset.filter(NO_ADHERENCIA=no_adherencia)
    if adherente:
        queryset = queryset.filter(REGISTRO_ADHERENCIA=adherente)
    if anio:
        try:
            queryset = queryset.filter(FECHA_ULTIMO_FOLIO__year=int(anio))
        except ValueError:
            pass
    if mes:
        try:
            queryset = queryset.filter(FECHA_ULTIMO_FOLIO__month=int(mes))
        except ValueError:
            pass

    # Paginación
    page = request.GET.get('page', 1)
    paginator = Paginator(queryset, 100)
    try:
        pacientes_paginados = paginator.page(page)
    except PageNotAnInteger:
        pacientes_paginados = paginator.page(1)
    except EmptyPage:
        pacientes_paginados = paginator.page(paginator.num_pages)

    # Filtros únicos
    sedes = Inmunoterapia.objects.exclude(SEDE__isnull=True).exclude(SEDE='')\
        .annotate(sede_upper=Upper('SEDE')).values_list('sede_upper', flat=True).distinct()

    clasificaciones = Inmunoterapia.objects.values_list('CLASIFICACION_TRATAMIENTO', flat=True).distinct().order_by('-CLASIFICACION_TRATAMIENTO')
    adherencias = Inmunoterapia.objects.exclude(NO_ADHERENCIA__isnull=True).exclude(NO_ADHERENCIA='').values_list('NO_ADHERENCIA', flat=True).distinct().order_by('NO_ADHERENCIA')
    adherente = Inmunoterapia.objects.exclude(REGISTRO_ADHERENCIA__isnull=True).exclude(REGISTRO_ADHERENCIA='').values_list('REGISTRO_ADHERENCIA', flat=True).distinct().order_by('-REGISTRO_ADHERENCIA')
    finalizaciones = Inmunoterapia.objects.values_list('FINALIZACION_TRATAMIENTO', flat=True).distinct().order_by('-FINALIZACION_TRATAMIENTO')
    finalizaciones = [f for f in finalizaciones if f]

    anios = Inmunoterapia.objects.exclude(FECHA_ULTIMO_FOLIO__isnull=True)\
        .annotate(anio=ExtractYear('FECHA_ULTIMO_FOLIO'))\
        .values_list('anio', flat=True).distinct().order_by('-anio')

    meses = Inmunoterapia.objects.exclude(FECHA_ULTIMO_FOLIO__isnull=True)\
        .annotate(mes=ExtractMonth('FECHA_ULTIMO_FOLIO'))\
        .values_list('mes', flat=True).distinct().order_by('mes')

    meses_nombres = {
        1: "ENERO", 2: "FEBRERO", 3: "MARZO", 4: "ABRIL",
        5: "MAYO", 6: "JUNIO", 7: "JULIO", 8: "AGOSTO",
        9: "SEPTIEMBRE", 10: "OCTUBRE", 11: "NOVIEMBRE", 12: "DICIEMBRE"
    }

    context = {
        'pacientes': pacientes_paginados,
        'sedes': sedes,
        'clasificaciones': clasificaciones,
        'adherencias': adherencias,
        'adherente': adherente,
        'finalizaciones': finalizaciones,
        'anios': anios,
        'meses': meses,
        'meses_nombres': meses_nombres,
    }
    return render(request, 'inmunoterapia/lista.html', context)

@login_required
def historico_inmunoterapia(request, IDSHARE):
    if not request.user.has_perm('inmunoterapia.ver_app_inmunoterapia'):
        return render(request, "401.html", status=401)
    
    try:
        historico = Inmunoterapia.objects.filter(IDSHARE=IDSHARE).order_by('-FECHA_ULTIMO_FOLIO')
        if not historico:
            return JsonResponse({'success': False, 'message': 'No se encontró el historial para este paciente.'}, status=404)
        print("📩 ID_SHARE recibido:", IDSHARE)
        print("📊 Cantidad registros:", historico.count())


        html = render_to_string('inmunoterapia/historico.html', {'historico': historico}, request=request)
        return JsonResponse({'success': True, 'html': html})
    except Exception as e:
        print("❌ ERROR EN VISTA HISTORICO:", str(e))
        return JsonResponse({'success': False, 'message': 'Error al cargar historial.'}, status=500)

@login_required
def cargar_edicion_inmunoterapia(request, idshare):
    if not request.user.has_perm('inmunoterapia.editar_inmunoterapia'):
        return HttpResponseForbidden("No tienes permiso para cambiar estado.")
    
    """Devuelve el formulario en formato JSON (HTML dentro del JSON)."""
    obj = get_object_or_404(Inmunoterapia, IDSHARE=idshare)
    adherente = Inmunoterapia.objects.exclude(REGISTRO_ADHERENCIA__isnull=True)\
        .exclude(REGISTRO_ADHERENCIA='')\
        .values_list('REGISTRO_ADHERENCIA', flat=True).distinct().order_by('-REGISTRO_ADHERENCIA')

    adherencias = Inmunoterapia.objects.exclude(NO_ADHERENCIA__isnull=True)\
        .exclude(NO_ADHERENCIA='')\
        .values_list('NO_ADHERENCIA', flat=True).distinct().order_by('NO_ADHERENCIA')

    html = render_to_string(
        "inmunoterapia/formulario_edicion.html",
        {"paciente": obj, "adherente": adherente, "adherencias": adherencias},
        request=request
    )

    return JsonResponse({"success": True, "html": html})

@login_required
@require_POST
def guardar_edicion_inmunoterapia(request, idshare):
    try:
        obj = get_object_or_404(Inmunoterapia, IDSHARE=idshare)

        # Actualizamos solo los campos permitidos
        obj.REGISTRO_ADHERENCIA = request.POST.get("registro_adherencia") or None
        obj.NO_ADHERENCIA = request.POST.get("no_adherencia") or None
        obj.OTROS = request.POST.get("observaciones") or None
        obj.FINALIZACION_TRATAMIENTO = request.POST.get("FINALIZACION_TRATAMIENTO") or None

        # Fecha próxima cita: solo se actualiza si viene en el POST
        fecha_proxima = request.POST.get("FECHA_PROXIMA_CITA")
        fecha_actualizada = False
        if fecha_proxima:
            obj.FECHA_PROXIMA_CITA = parse_date(fecha_proxima)
            fecha_actualizada = True

        # Lógica de clasificación según registro de adherencia
        val = (obj.REGISTRO_ADHERENCIA or "").strip().lower()
        if val in ["si", "no", "no aplica"]:
            obj.CLASIFICACION_TRATAMIENTO = "Clasificado"
        else:
            obj.CLASIFICACION_TRATAMIENTO = "No clasificado"

        # Guardamos solo los campos que realmente cambian
        update_fields = [
            "REGISTRO_ADHERENCIA",
            "NO_ADHERENCIA",
            "OTROS",
            "CLASIFICACION_TRATAMIENTO",
            "FINALIZACION_TRATAMIENTO",
        ]
        if fecha_actualizada:
            update_fields.append("FECHA_PROXIMA_CITA")

        obj.save(update_fields=update_fields)

        return JsonResponse({"success": True, "estado_clasificacion": obj.CLASIFICACION_TRATAMIENTO})

    except Exception as e:
        print(traceback.format_exc())
        return HttpResponseBadRequest(f"Error al guardar: {str(e)}")
    

@login_required    
def cargar_agregar_inmunoterapia(request, idshare):
    if not request.user.has_perm('inmunoterapia.agregar_inmunoterapia'):
        return HttpResponseForbidden("No tienes permiso para agregar estado.")
    """Devuelve el formulario en formato JSON (HTML dentro del JSON)."""
    obj = get_object_or_404(Inmunoterapia, IDSHARE=idshare)
    adherente = Inmunoterapia.objects.exclude(REGISTRO_ADHERENCIA__isnull=True)\
        .exclude(REGISTRO_ADHERENCIA='')\
        .values_list('REGISTRO_ADHERENCIA', flat=True).distinct().order_by('-REGISTRO_ADHERENCIA')

    adherencias = Inmunoterapia.objects.exclude(NO_ADHERENCIA__isnull=True)\
        .exclude(NO_ADHERENCIA='')\
        .values_list('NO_ADHERENCIA', flat=True).distinct().order_by('NO_ADHERENCIA')

    html = render_to_string(
        "inmunoterapia/formulario_agregar.html",
        {"paciente": obj, "adherente": adherente, "adherencias": adherencias},
        request=request
    )

    return JsonResponse({"success": True, "html": html})

@login_required
@require_POST
def guardar_agregar_inmunoterapia(request, idshare):
    try:
        obj = get_object_or_404(Inmunoterapia, IDSHARE=idshare)

        # Actualizamos solo los campos permitidos
        obj.REGISTRO_ADHERENCIA = request.POST.get("registro_adherencia") or None
        obj.NO_ADHERENCIA = request.POST.get("no_adherencia") or None
        obj.OTROS = request.POST.get("observaciones") or None
        obj.FINALIZACION_TRATAMIENTO = request.POST.get("FINALIZACION_TRATAMIENTO") or None

        # Fecha próxima cita: solo se actualiza si viene en el POST
        fecha_proxima = request.POST.get("FECHA_PROXIMA_CITA")
        fecha_actualizada = False
        if fecha_proxima:
            obj.FECHA_PROXIMA_CITA = parse_date(fecha_proxima)
            fecha_actualizada = True

        # Lógica de clasificación según registro de adherencia
        val = (obj.REGISTRO_ADHERENCIA or "").strip().lower()
        if val in ["si", "no", "no aplica"]:
            obj.CLASIFICACION_TRATAMIENTO = "Clasificado"
        else:
            obj.CLASIFICACION_TRATAMIENTO = "No clasificado"
        
        # Modificado siempre
        obj.MODIFICADO = now()
        obj.MODIFICADO_POR = request.user.username if request.user.is_authenticated else "Sistema"

            
        # Guardamos solo los campos que realmente cambian
        update_fields = [
            "REGISTRO_ADHERENCIA",
            "NO_ADHERENCIA",
            "OTROS",
            "CLASIFICACION_TRATAMIENTO",
            "FINALIZACION_TRATAMIENTO",
            "MODIFICADO",
            "MODIFICADO_POR"
        ]
        if fecha_actualizada:
            update_fields.append("FECHA_PROXIMA_CITA")

        obj.save(update_fields=update_fields)

        return JsonResponse({"success": True, "estado_clasificacion": obj.CLASIFICACION_TRATAMIENTO})

    except Exception as e:
        print(traceback.format_exc())
        return HttpResponseBadRequest(f"Error al guardar: {str(e)}")
    