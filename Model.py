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
    # day = days[0]                                   # Jeden dzie?? 0-obecny 1-jutro
    # day_temp = day["temp"]                          # Temperatury w ci??gu dnia
    # day_weather = day["weather"]                    # Opis pogody
    # day_pop = day["pop"]                            # Prawdopodobie??stwo opad??w
    # day_temp_min = day_temp["min"]                  # Minimalna temperatura w ci??gu dnia
    # day_temp_max = day_temp["max"]                  # Maksymalna temperatura w ci??gu dnia

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
            "Sp??dnice | Spodenki": 0
            },
        "Bielizna":{ 
            "Majtki": 0, 
            "Skarpetki": 0,
            "Pi??ama": 0
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
            weather_list.append("mro??no")
        elif (morn_temperature < 5):
            weather_list.append("zimno")
        elif (day_temperature < 18):
            weather_list.append("ch??odno")
        elif (day_temperature < 25):
            weather_list.append("ciep??o")  
        else:
            weather_list.append("gor??co")

    for i in range(start_time, end_time + 1):
        weather = days[i]["weather"][0]
        main_weather = weather["main"]

        if(main_weather == "Rain"):
            items_list["Akcesoria"].append("parasol")

            if(weather_list[i] != "mro??no" and weather_list[i] !="zimno"):
                items_list["Kurtki"].append("kurtka przeciwdeszczowa")
            break      


    items_list["Inne"].append("portfel")
    items_list["Inne"].append("s??uchawki")
    items_list["Inne"].append("power bank")

    if(trip_length > 0):
        cold_days = weather_list.count("mro??no") + weather_list.count("zimno") + weather_list.count("ch??odno") - 1
        if(cold_days < 0):
            cold_days = 0
        hot_days = trip_length - cold_days

        items_list["Inne"].append("??adowarka")

        items_list["Kosmetyczka"].append("szczoteczka do z??b??w")
        items_list["Kosmetyczka"].append("pasta do z??b??w")
        items_list["Kosmetyczka"].append("szampon")
        items_list["Kosmetyczka"].append("dezodorant")
        items_list["Inne"].append("plastry")
        items_list["Bielizna"]["Pi??ama"] = 1
        items_list["Bielizna"]["Majtki"] = trip_length
        items_list["Bielizna"]["Skarpetki"] = trip_length
        items_list["Ubrania"]["Koszulki"] = trip_length
        items_list["Ubrania"]["Bluzy | Swetry"] = int(cold_days/2) + int(hot_days/3)
        items_list["Ubrania"]["Spodnie"] = int(cold_days/2)
        items_list["Ubrania"]["Sp??dnice | Spodenki"] = int(hot_days/2)

        if(accomodation_type == "Biwak"):
            items_list["Biwak"].append("namiot")
            items_list["Biwak"].append("latarka")
            items_list["Biwak"].append("??piw??r")
            items_list["Biwak"].append("poduszka")
            items_list["Biwak"].append("termos")

        if(accomodation_type != "Hotel"):
            items_list["Akcesoria"].append("r??cznik")
            items_list["Kosmetyczka"].append("myd??o")

    if("Mro??no" in weather_list):
        items_list["Akcesoria"].append("szalik")
        items_list["Akcesoria"].append("r??kawiczki")

    if("Zimno" in weather_list or "mro??no" in weather_list):
        items_list["Buty"].append("buty zimowe")
        items_list["Kurtki"].append("kurtka zimowa")

    if("Ch??odno" in weather_list):
        items_list["Buty"].append("adidasy")
        items_list["Kurtki"].append("lekka kurtka")

    if("Ciep??o" in weather_list):
        items_list["Buty"].append("lekkie buty")

    if("Gor??co" in weather_list):
        items_list["Buty"].append("sanda??y")
        items_list["Akcesoria"].append("okulary przeciws??oneczne")
        items_list["Akcesoria"].append("letnia czapka/kapelusz")
        items_list["Kosmetyczka"].append("krem z filtrem")

    if ("G??ry" in attractions):
        items_list["G??ry"] = []
        items_list["G??ry"].append("plecak")
        items_list["G??ry"].append("buty g??rskie")
        items_list["G??ry"].append("mapa")
        items_list["G??ry"].append("bidon")

    if ("Sporty zimowe narty" in attractions):
        items_list["Sporty zimowe"] = []
        items_list["Sporty zimowe"].append("kask narciarski")
        items_list["Sporty zimowe"].append("gogle")
        items_list["Sporty zimowe"].append("narty")
        items_list["Sporty zimowe"].append("buty narciarskie")
        items_list["Sporty zimowe"].append("grube r??kawiczki")
        items_list["Sporty zimowe"].append("skarpety narciarskie")
        items_list["Sporty zimowe"].append("kombinezon narciarski")

    if ("Sporty zimowe snowboard" in attractions):
        items_list["Sporty zimowe"] = []
        items_list["Sporty zimowe"].append("snowboard")
        items_list["Sporty zimowe"].append("wi??zania")
        items_list["Sporty zimowe"].append("kask snowboardowy")
        items_list["Sporty zimowe"].append("grube r??kawiczki")
        items_list["Sporty zimowe"].append("gogle")
        items_list["Sporty zimowe"].append("buty snowboardowe")
        items_list["Sporty zimowe"].append("skarpety snowboardowe")
        items_list["Sporty zimowe"].append("spodnie snowboardowe")

    if ("Atrakcje wodne" in attractions):
        items_list["Do p??ywania"] = []
        items_list["Do p??ywania"].append("str??j k??pielowy")
        items_list["Do p??ywania"].append("klapki")
        items_list["Do p??ywania"].append("okulary do p??ywania")
        items_list["Do p??ywania"].append("r??cznik pla??owy")

    if ("Zwiedzanie" in attractions):
        items_list["Zwiedzanie"] = []
        items_list["Zwiedzanie"].append("przewodnik")
        items_list["Zwiedzanie"].append("got??wka")
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

    
 