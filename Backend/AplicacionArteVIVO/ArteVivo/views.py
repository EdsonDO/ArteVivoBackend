from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def vista_formulario(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        edad = request.POST.get('edad')
        return JsonResponse({'mensaje': 'Datos recibidos', 'nombre': nombre, 'edad': edad})
    return JsonResponse({'formulario': 'Envía nombre y edad con POST'})

def vista_tabla(request):
    datos = [
        {'nombre': 'Juan', 'edad': 20},
        {'nombre': 'Ana', 'edad': 22},
        {'nombre': 'Luis', 'edad': 21},
    ]
    return JsonResponse({'usuarios': datos})
