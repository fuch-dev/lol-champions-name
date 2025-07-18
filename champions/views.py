import requests
from django.shortcuts import render

# Función para obtener la última versión del juego
def get_latest_version():
    try:
        version_url = "https://ddragon.leagueoflegends.com/api/versions.json"
        response = requests.get(version_url)
        response.raise_for_status() # Lanza un error si la petición falla
        return response.json()[0] # La primera versión de la lista es la más reciente
    except requests.exceptions.RequestException as e:
        print(f"Error fetching latest version: {e}")
        return "14.14.1" # Una versión de respaldo por si falla la API

def champion_list(request):
    version = get_latest_version()
    # URL de la API de DDragon para obtener todos los campeones en español (México)
    url = f"https://ddragon.leagueoflegends.com/cdn/{version}/data/es_MX/champion.json"
    
    champion_names = []
    error_message = None

    try:
        # Hacemos la petición a la API
        response = requests.get(url)
        response.raise_for_status() # Lanza un error para códigos 4xx/5xx

        # Extraemos el JSON de la respuesta
        data = response.json()
        
        # El JSON tiene una llave 'data' que contiene a todos los campeones
        # Extraemos solo los nombres y los guardamos en una lista
        champions_data = data['data'].values()
        champion_names = sorted([champion['name'] for champion in champions_data])

    except requests.exceptions.RequestException as e:
        # Manejo de errores de conexión o de la API
        error_message = f"No se pudo conectar a la API de Riot: {e}"
        
    except KeyError:
        # Manejo de errores si la estructura del JSON cambia
        error_message = "Error al procesar los datos de los campeones. La estructura del JSON puede haber cambiado."

    # Preparamos el contexto para pasarlo a la plantilla
    context = {
        'champions': champion_names,
        'error': error_message
    }
    
    # Renderizamos la plantilla HTML con el contexto
    return render(request, 'champions/champion_list.html', context)