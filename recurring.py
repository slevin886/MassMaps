"""
This script runs on a cronjob to collect travel times at regular intervals and write them to
the database.
"""
import os
import django
import re
from typing import List
from datetime import datetime
import pytz
from google_distance import GoogleDistance, TravelTime
from google_distance.origin_locations import origins as CITIES


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mass_maps.settings")
django.setup()

from app_maps.models import Commute, Origins


class WriteDistances:

    def __init__(self, origins=CITIES):
        self.origins = origins
        self.time_zone = pytz.timezone('US/Eastern')
        self.api_key = os.getenv('API_KEY')
        self.pattern = r"^(.*,\s..?)(\s..|,\s)"

    def get_data(self, mode: str) -> List[TravelTime]:
        locations = []
        for org in self.origins:
            if datetime.now(tz=self.time_zone).hour < 12:
                locations.append(
                    {'origin': org, 'destination': '1 City Hall Square, Boston, Massachusetts'}
                )
            else:
                locations.append(
                    {'destination': org, 'origin': '1 City Hall Square, Boston, Massachusetts'}
                )
        dist = GoogleDistance(self.api_key, mode=mode)
        results = dist.run_async(locations)
        return results

    def write_travel_times_to_db(self):
        errors = []
        for mode in ['driving', 'transit']:
            results = self.get_data(mode)
            for result in results:
                if result.success:
                    if result.origin[0] == '1':
                        origin = self.clean_result_name(result.destination)
                    else:
                        origin = self.clean_result_name(result.origin)
                    origin_object = Origins.objects.get(name=origin)
                    if not origin_object:
                        errors.append(origin)
                    commute = Commute(
                        origin=origin_object,
                        distance=result.miles,
                        duration=result.minutes,
                        mode=mode,
                        in_traffic=result.duration_in_traffic if hasattr(result, 'duration_in_traffic') else None,
                        date=datetime.now(tz=self.time_zone)
                    )
                    commute.save()
                else:
                    errors.append(f"{result.origin} to {result.destination}: {result.status}")
        print('Finished cronjob and writing to database')
        if errors:
            print("The following errors occurred:\n" + "\n".join(errors))


    @staticmethod
    def clean_result_name(location: str) -> str:
        """
        Changes the google generated location to the syntax expected by the database
        """
        if location[0] == '1':  # captures Boston
            return location
        return re.findall(r"^(.*,\s..?)(\s..|,\s)", location)[0][0]


if __name__ == '__main__':
    print(f'Starting API queries and DB writes at {datetime.now()}')
    writing = WriteDistances()
    writing.write_travel_times_to_db()
