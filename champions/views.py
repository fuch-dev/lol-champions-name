import requests
from django.http import JsonResponse

def get_latest_version():
    try:
        version_url = "https://ddragon.leagueoflegends.com/api/versions.json"
        response = requests.get(version_url)
        response.raise_for_status()
        return response.json()[0]
    except requests.exceptions.RequestException as e:
        return "14.14.1"

def champion_search(request, search_term):
    version = get_latest_version()
    
    url = f"https://ddragon.leagueoflegends.com/cdn/{version}/data/es_MX/champion.json"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        champion_names = [champion['name'] for champion in data['data'].values()]
        search_term_lower = search_term.lower()
        matches = [
            name for name in champion_names 
            if search_term_lower in name.lower()
        ]

        return JsonResponse({'matches': sorted(matches)})
    
    except requests.exceptions.RequestException:
        return JsonResponse({'error': 'Failed to connect to Riot API'}, status=503)
    
    except KeyError:
        return JsonResponse({'error': 'Error processing champions data'}, status=500)