"""
Used to populate database with csv data collected prior to creation of the web app.

Assumes that 'commute_info.csv' (commute data) and 'lat_lng.csv' (origin locations) are
located in project root directory.
"""
import os
import pandas as pd
import re
import django
import pytz

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mass_maps.settings")
django.setup()

from app_maps.models import Origins, Commute

PATTERN = r"^(.*,\s..?)(\s..|,\s)"


def clean_names(location: str) -> str:
    if location[0] == '1':
        return location
    return re.findall(PATTERN, location)[0][0]


def manipulate_df(file):
    df = pd.read_csv(file)
    df = df.reset_index(drop=True)
    df = df.drop(df.loc[df['status'] != 'OK'].index)
    df['origin'] = df['origin'].apply(clean_names)
    df['destination'] = df['destination'].apply(clean_names)
    df['duration_in_traffic'] = df['duration_in_traffic'].fillna(0).astype(int)
    df['utc_time_created'] = pd.to_datetime(df['utc_time_created']).dt.round('min')
    my_timezone = pytz.timezone('UTC')
    df['utc_time_created'] = df['utc_time_created'].dt.tz_localize(my_timezone)
    my_timezone = pytz.timezone('America/New_York')
    df['utc_time_created'] = df['utc_time_created'].dt.tz_convert(my_timezone)
    return df


def write_to_origins_db(file):
    df = pd.read_csv(file).to_dict(orient='records')
    for loc in df:
        origin = Origins(
            name=loc['name'],
            latitude=loc['latitude'],
            longitude=loc['longitude'],
        )
        origin.save()
    print('Finished writing origins')


def write_to_commutes_db(df):
    names = [i for i in df['origin'].unique() if i[0] != '1']
    for name in names:
        origin_object = Origins.objects.get(name=name)
        # the time will indicate if the origin is Boston- collecting the commute locations only
        commutes = df.loc[(df['origin'] == name) | (df['destination'] == name)].to_dict(orient='records')
        for comm in commutes:
            new_commute = Commute(
                origin=origin_object,
                distance=comm['distance'],
                duration=comm['duration'],
                mode=comm['mode'],
                in_traffic=comm['duration_in_traffic'],
                date=comm['utc_time_created']
            )
            new_commute.save()
    print('Finished writing commutes')


if __name__ == '__main__':
    base_dir = os.path.dirname(os.path.realpath(__file__))
    write_to_origins_db(os.path.join(base_dir, 'lat_lng.csv'))
    data = manipulate_df(os.path.join(base_dir, 'clean_mass_data.csv'))
    write_to_commutes_db(data)
