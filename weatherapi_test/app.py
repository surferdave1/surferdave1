from __future__ import print_function
import time
import weatherapi
from weatherapi.rest import ApiException
from pprint import pprint

# Configure API key authorization: ApiKeyAuth
configuration = weatherapi.Configuration()
configuration.api_key['key'] = '12c96143c1c24894836214843252908'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['key'] = 'Bearer'

# create an instance of the API class
api_instance = weatherapi.APIsApi(weatherapi.ApiClient(configuration))
q = 'indianapolis, Indiana' # str | Pass US Zipcode, UK Postcode, Canada Postalcode, IP address, Latitude/Longitude (decimal degree) or city name. Visit [request parameter section](https://www.weatherapi.com/docs/#intro-request) to learn more.
days = 1 # int | Number of days of weather forecast. Value ranges from 1 to 14
dt = '2025-09-29' # date | Date should be between today and next 14 day in yyyy-MM-dd format. e.g. '2015-01-01' (optional)


try:
    # Forecast API
    api_response = api_instance.forecast_weather(q, days, dt=dt)
    #pprint(api_response)

except ApiException as e:
    print("Exception when calling APIsApi->forecast_weather: %s\n" % e)
# Extract several values at once
city = api_response['location']['name']  # type: ignore
current_temp = api_response['current']['temp_c']  # type: ignore
current_humidity = api_response['current']['humidity']  # type: ignore
forecast_day = api_response['forecast']['forecastday'][0]  # type: ignore
max_temp = forecast_day['day']['maxtemp_c'] # pyright: ignore[reportArgumentType]
print(f"City: {city}, Current Temp: {current_temp}°C, Humidity: {current_humidity}%, Max Temp Today: {max_temp}°C")
