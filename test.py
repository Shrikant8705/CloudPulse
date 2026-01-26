#Basic script 
def check_weather(rain,humidity):
    if rain > 30 and humidity > 65:
        print("WARNING: High risk of a flash flood or a Cloudburst!")
    else:
        print("Weather seems to be clear!")


usr_rainfall=int(input("Please enter the rainfall in your area:\n"))
usr_humidity=int(input("Please enter humidity in your area:\n"))

status = check_weather(usr_rainfall,usr_humidity)
print(status)