from django.contrib.auth.decorators import login_required

from ..services import *


@login_required
def clean_data(request):
    is_superuser = request.user.is_superuser

    if not is_superuser:
        return JsonResponse({'error': 'Unauthorized'}, status=401)

    df = get_sensor_data_as_dataframe()
    if df is None:
        return JsonResponse({'error': 'No se pudieron obtener los datos para limpiar'}, status=500)

    cleaner = DiagnosticDataCleaner(df)
    result = cleaner.clean_and_validate_data()

    if result.is_failure:
        return JsonResponse({'errors': result.errors}, status=400)
    else:
        for item in result.value:
            newResult = insert_clean_data(item)
            if newResult is None:
                return JsonResponse({'message': 'Something went wrong!'}, status=500)
        return JsonResponse({'message': 'Data cleaned successfully'}, status=200)