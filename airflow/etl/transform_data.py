import os
import pandas as pd
from datetime import datetime

s3_bucket_name = os.environ.get('AWS_S3_BUCKET_NAME')

def kelvin_to_celsius(temp):
    return temp - 273.15

def transform_weather_data(ti):
    data = ti.xcom_pull(task_ids='extract_weather_data')
    city = data['name']
    weather_desc = data['weather'][0]['description']
    temp = kelvin_to_celsius(data['main']['temp'])
    feels_like = kelvin_to_celsius(data['main']['feels_like'])
    min_temp = kelvin_to_celsius(data['main']['temp_min'])
    max_temp = kelvin_to_celsius(data['main']['temp_max'])
    pressure = data['main']['pressure']
    humidity = data['main']['humidity']
    wind_speed = data['wind']['speed']
    time_of_record = datetime.fromtimestamp(data['dt'] + data['timezone'])
    sunrise_time = datetime.fromtimestamp(data['sys']['sunrise'] + data['timezone'])
    sunset_time = datetime.fromtimestamp(data['sys']['sunset'] + data['timezone'])

    transformed_data = {
        'City': city,
        'Weather Description': weather_desc,
        'Temperature (C)': temp,
        'Feels Like (C)': feels_like,
        'Minimum Temperature (C)': min_temp,
        'Maximum Temperature (C)': max_temp,
        'Pressure': pressure,
        'Humidity': humidity,
        'Wind Speed': wind_speed,
        'Time of Record': time_of_record,
        'Sunrise Time (Local Time)': sunrise_time,
        'Sunset Time (Local Time)': sunset_time
    }

    transformed_df = pd.DataFrame(transformed_data, index=[0])
    return transformed_df

def save_to_s3(ti):
    df = ti.xcom_pull(task_ids='transform_weather_data')
    city = df['City'][0]
    filename = f"current_weather_{city}_{datetime.now().strftime('%d-%m-%Y-%H-%M-%S')}"
    df.to_csv(f"s3://{s3_bucket_name}/{filename}.csv", index=False)