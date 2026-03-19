from django.http import JsonResponse
from ia_assistant.services import consultar_ia_con_datos

def api_consultar_ia(request):
    # Obtenemos la pregunta que viene del JavaScript (?pregunta=...)
    pregunta = request.GET.get('pregunta', None)
    
    if not pregunta:
        return JsonResponse({'respuesta': 'No recibí ninguna pregunta.'}, status=400)
    
    # Llamamos a tu función pro que lee la base de datos
    resultado = consultar_ia_con_datos(pregunta)
    
    return JsonResponse({'respuesta': resultado})