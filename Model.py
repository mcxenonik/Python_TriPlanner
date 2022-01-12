import requests
# import json
# from math import ceil, floor


# current_weather = get_current_weather_by_city_name(city_name, api_key)

# with open('current_weather.json', 'w') as file:
#     json.dump(current_weather, file)

# print(current_weather)


# forecast_5_days_weather = get_forecast_5_days_weather_by_city_name(city_name, api_key)

# with open('forecast_5_days_weather.json', 'w') as file:
#     json.dump(forecast_5_days_weather, file)

# print(forecast_5_days_weather)


# def get_current_weather_by_city_name(city_name, api_key):
#     url = "http://api.openweathermap.org/data/2.5/weather?q={city_name}&units=metric&lang=pl&appid={API_key}"

#     response = requests.get(url.format(city_name=city_name, API_key=api_key)).json()

#     return response


# def get_forecast_5_days_weather_by_city_name(city_name, api_key):
#     url = "http://api.openweathermap.org/data/2.5/forecast?q={city_name}&units=metric&lang=pl&appid={API_key}"

#     response = requests.get(url.format(city_name=city_name, API_key=api_key)).json()

#     return response



def get_city_cords_by_city_name(city_name):
    api_key = "036f8ef858d41dcd62395b79cacc1a55"
    url = "http://api.openweathermap.org/data/2.5/weather?q={city_name}&units=metric&lang=pl&appid={API_key}"

    response = requests.get(url.format(city_name=city_name, API_key=api_key)).json()

    if(response["cod"] == "404"):
        return None

    cords = (float(response["coord"]["lat"]), float(response["coord"]["lon"]))

    # print(cords)

    return cords


def get_places(city_cords, api_key):
    radius = 1000
    url = "http://api.opentripmap.com/0.1/en/places/radius?radius={radius}&lon={city_lon}&lat={city_lat}&format=json&apikey={API_key}"

    response = requests.get(url.format(radius=radius, city_lat=city_cords[0], city_lon=city_cords[1], API_key=api_key)).json()

    return response

def get_forecast_7_days_weather_by_city_cords(city_cords):
    api_key = "036f8ef858d41dcd62395b79cacc1a55"
    url = "https://api.openweathermap.org/data/2.5/onecall?lat={city_lat}&lon={city_lon}&exclude=current,minutely,hourly,alerts&units=metric&lang=pl&appid={API_key}"

    response = requests.get(url.format(city_lat=city_cords[0], city_lon=city_cords[1], API_key=api_key)).json()

    return response




def prepare_items_list(city_cords, start_time=1, trip_length=4, accomodation_type="Inne", attracts=["Zwiedzanie"]):
    forecast_7_days_weather = get_forecast_7_days_weather_by_city_cords(city_cords)

    # with open('forecast_7_days_weather.json', 'w') as file:
    #     json.dump(forecast_7_days_weather, file)

    days = forecast_7_days_weather["daily"]         # Lista dni (0-7)
    # day = days[0]                                   # Jeden dzień 0-obecny 1-jutro
    # day_temp = day["temp"]                          # Temperatury w ciągu dnia
    # day_weather = day["weather"]                    # Opis pogody
    # day_pop = day["pop"]                            # Prawdopodobieństwo opadów
    # day_temp_min = day_temp["min"]                  # Minimalna temperatura w ciągu dnia
    # day_temp_max = day_temp["max"]                  # Maksymalna temperatura w ciągu dnia

    ###################ANKIETA

    end_time = start_time + trip_length
    print("end_time",end_time)

    attractions = attracts
    weather_list = []
    # accomodation_type = ""

    ##################

    items_list = {
        "Buty":[], 
        "Kurtki":[], 
        "Kosmetyczka":[], 
        "Akcesoria":[],
        "Ubrania": {
            "Koszulki": 0, 
            "Bluzy | Swetry": 0,  
            "Spodnie": 0, 
            "Spódnice | Spodenki": 0
            },
        "Bielizna":{ 
            "Majtki": 0, 
            "Skarpetki": 0,
            "Piżama": 0
            },
        "Inne":[]

    }

    

    for i in range(start_time, end_time + 1):
        feels_like = days[i]["feels_like"]
        morn_temperature = feels_like["morn"]
        day_temperature = feels_like["day"]
        print(feels_like)
        weather = days[i]["weather"][0]
        main_weather = weather["main"]

        if (morn_temperature < -5):
            weather_list.append("mroźno")
        elif (morn_temperature < 5):
            weather_list.append("zimno")
        elif (day_temperature < 18):
            weather_list.append("chłodno")
        elif (day_temperature < 25):
            weather_list.append("ciepło")  
        else:
            weather_list.append("gorąco")

    for i in range(start_time, end_time + 1):
        weather = days[i]["weather"][0]
        main_weather = weather["main"]

        if(main_weather == "Rain"):
            items_list["Akcesoria"].append("parasol")

            if(weather_list[i] != "mroźno" and weather_list[i] !="zimno"):
                items_list["Kurtki"].append("kurtka przeciwdeszczowa")
            break      


    items_list["Inne"].append("portfel")
    items_list["Inne"].append("słuchawki")
    items_list["Inne"].append("power bank")

    if(trip_length > 0):
        cold_days = weather_list.count("mroźno") + weather_list.count("zimno") + weather_list.count("chłodno") - 1
        if(cold_days < 0):
            cold_days = 0
        hot_days = trip_length - cold_days

        items_list["Inne"].append("ładowarka")

        items_list["Kosmetyczka"].append("szczoteczka do zębów")
        items_list["Kosmetyczka"].append("pasta do zębów")
        items_list["Kosmetyczka"].append("szampon")
        items_list["Kosmetyczka"].append("dezodorant")
        items_list["Inne"].append("plastry")
        items_list["Bielizna"]["Piżama"] = 1
        items_list["Bielizna"]["Majtki"] = trip_length
        items_list["Bielizna"]["Skarpetki"] = trip_length
        items_list["Ubrania"]["Koszulki"] = trip_length
        items_list["Ubrania"]["Bluzy | Swetry"] = int(cold_days/2) + int(hot_days/3)
        items_list["Ubrania"]["Spodnie"] = int(cold_days/2)
        items_list["Ubrania"]["Spódnice | Spodenki"] = int(hot_days/2)

        if(accomodation_type == "Biwak"):
            items_list["Biwak"].append("namiot")
            items_list["Biwak"].append("latarka")
            items_list["Biwak"].append("śpiwór")
            items_list["Biwak"].append("poduszka")
            items_list["Biwak"].append("termos")

        if(accomodation_type != "Hotel"):
            items_list["Akcesoria"].append("ręcznik")
            items_list["Kosmetyczka"].append("mydło")

    if("Mroźno" in weather_list):
        items_list["Akcesoria"].append("szalik")
        items_list["Akcesoria"].append("rękawiczki")

    if("Zimno" in weather_list or "mroźno" in weather_list):
        items_list["Buty"].append("buty zimowe")
        items_list["Kurtki"].append("kurtka zimowa")

    if("Chłodno" in weather_list):
        items_list["Buty"].append("adidasy")
        items_list["Kurtki"].append("lekka kurtka")

    if("Ciepło" in weather_list):
        items_list["Buty"].append("lekkie buty")

    if("Gorąco" in weather_list):
        items_list["Buty"].append("sandały")
        items_list["Akcesoria"].append("okulary przeciwsłoneczne")
        items_list["Akcesoria"].append("letnia czapka/kapelusz")
        items_list["Kosmetyczka"].append("krem z filtrem")

    if ("Góry" in attractions):
        items_list["Góry"] = []
        items_list["Góry"].append("plecak")
        items_list["Góry"].append("buty górskie")
        items_list["Góry"].append("mapa")
        items_list["Góry"].append("bidon")

    if ("Sporty zimowe narty" in attractions):
        items_list["Sporty zimowe"] = []
        items_list["Sporty zimowe"].append("kask narciarski")
        items_list["Sporty zimowe"].append("gogle")
        items_list["Sporty zimowe"].append("narty")
        items_list["Sporty zimowe"].append("buty narciarskie")
        items_list["Sporty zimowe"].append("grube rękawiczki")
        items_list["Sporty zimowe"].append("skarpety narciarskie")
        items_list["Sporty zimowe"].append("kombinezon narciarski")

    if ("Sporty zimowe snowboard" in attractions):
        items_list["Sporty zimowe"] = []
        items_list["Sporty zimowe"].append("snowboard")
        items_list["Sporty zimowe"].append("wiązania")
        items_list["Sporty zimowe"].append("kask snowboardowy")
        items_list["Sporty zimowe"].append("grube rękawiczki")
        items_list["Sporty zimowe"].append("gogle")
        items_list["Sporty zimowe"].append("buty snowboardowe")
        items_list["Sporty zimowe"].append("skarpety snowboardowe")
        items_list["Sporty zimowe"].append("spodnie snowboardowe")

    if ("Atrakcje wodne" in attractions):
        items_list["Do pływania"] = []
        items_list["Do pływania"].append("strój kąpielowy")
        items_list["Do pływania"].append("klapki")
        items_list["Do pływania"].append("okulary do pływania")
        items_list["Do pływania"].append("ręcznik plażowy")

    if ("Zwiedzanie" in attractions):
        items_list["Zwiedzanie"] = []
        items_list["Zwiedzanie"].append("przewodnik")
        items_list["Zwiedzanie"].append("gotówka")
        items_list["Zwiedzanie"].append("nerka/saszetka")
        items_list["Zwiedzanie"].append("mokre chusteczki")


    print(weather_list)
    return(items_list)



if __name__ == "__main__":
    api_key_weather = "036f8ef858d41dcd62395b79cacc1a55"
    api_key_places = "5ae2e3f221c38a28845f05b6e92a37ce65de0feaa7d4368e7986d538"

    city_name = "Warszawa"                      # London itp.
    city_cords = ("52.2298", "21.0118")         # Warszawa

    # get_city_cords_by_city_name(city_name, api_key_weather)

    interesting_places = get_places(city_cords, api_key_places)

    # with open('interesting_places.json', 'w') as file:
    #     json.dump(interesting_places, file)

    prepare_items_list(city_cords)

    
 