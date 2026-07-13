import json
import urllib.request
import urllib.parse
import math

class HospitalFinder:
    def __init__(self):
        self.overpass_url = "http://overpass-api.de/api/interpreter"

    def haversine(self, lat1, lon1, lat2, lon2):
        # Calculate the great circle distance between two points
        # on the earth (specified in decimal degrees)
        R = 6371000 # Radius of earth in meters
        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)
        delta_phi = math.radians(lat2 - lat1)
        delta_lambda = math.radians(lon2 - lon1)

        a = math.sin(delta_phi / 2.0) ** 2 + \
            math.cos(phi1) * math.cos(phi2) * \
            math.sin(delta_lambda / 2.0) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c

    def find_nearest_hospitals(self, lat: float, lon: float, radius: int = 5000, limit: int = 3) -> list:
        query = f"""
        [out:json][timeout:10];
        (
          node["amenity"="hospital"](around:{radius},{lat},{lon});
          way["amenity"="hospital"](around:{radius},{lat},{lon});
          relation["amenity"="hospital"](around:{radius},{lat},{lon});
        );
        out center;
        """
        
        try:
            headers = {'User-Agent': 'AgenticHealthChecker/1.0'}
            payload = urllib.parse.urlencode({'data': query}).encode('utf-8')
            req = urllib.request.Request(self.overpass_url, data=payload, headers=headers)
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode('utf-8'))
                
            hospitals = []
            for element in data.get('elements', []):
                hosp_lat = element.get('lat')
                hosp_lon = element.get('lon')
                
                # If it's a way/relation, it might have a 'center'
                if not hosp_lat and 'center' in element:
                    hosp_lat = element['center'].get('lat')
                    hosp_lon = element['center'].get('lon')
                    
                if hosp_lat and hosp_lon:
                    dist = self.haversine(lat, lon, hosp_lat, hosp_lon)
                    tags = element.get('tags', {})
                    name = tags.get('name', 'Unknown Hospital')
                    
                    # Rough walking time estimate: average walking speed 1.4 m/s
                    # Rough driving time estimate: average city driving 8.3 m/s (30 km/h)
                    driving_time_mins = max(1, int(dist / 8.3 / 60))
                    
                    hospitals.append({
                        "name": name,
                        "distance_meters": int(dist),
                        "estimated_driving_time_mins": driving_time_mins
                    })
                    
            # Sort by distance
            hospitals.sort(key=lambda x: x['distance_meters'])
            
            # Return top N
            return hospitals[:limit]
            
        except Exception as e:
            print(f"Hospital Finder Error: {e}")
            return []
