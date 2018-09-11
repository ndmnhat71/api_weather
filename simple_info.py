import json
import sys
import api_weather
import argparse


def getOptions():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-name', nargs='+',
                       help='Request by city name. Ex: "-name Goeteborg" se"')
    group.add_argument('-zip', nargs='+',
                       help='Request by ZIP code and country. Ex: "-zip 94040 us"')
    group.add_argument("-coord", nargs='+',
                       help='Request by coordinates. Ex: "-coord 11.91667, 57.700001"')
    group.add_argument("-id", nargs='?',
                       help='Request for a city ID. Ex: "-id 2711537"')
    parser.add_argument('-token', nargs='?',
                        default='d102d990454611358a50303812839a4d',
                        help="Change API token")
    parser.add_argument('-unit', nargs='?',
                        help='Change units type. Ex: "-unit metric')
    return parser.parse_args()


def prepareAndPrint(data, remindString, tempString, windSpeedString):
    # Prepare variables
    currentTemp = str(data['main']['temp']) + tempString
    currentCity = data['name']
    currentCountry = data['sys']['country']
    currentHumidity = str(data['main']['humidity']) + "%"
    currentVisibility = str(data['visibility']) + "m"
    currentWindSpeed = str(data['wind']['speed']) + " " + windSpeedString
    weatherMain = data['weather'][0]['main']
    weatherDescription = data['weather'][0]['description']

    # Prepare strings
    headline1 = "The current conditions in {}, {} is: {} - {}".format(
        currentCity, currentCountry, weatherMain, weatherDescription)

    headline2 = "| Temperature | Humidity |   Wind Speed   | Visibility |"

    # Print strings
    print(headline1)
    print(headline2)
    print("|{:^13}|{:^10}|{:^16}|{:^12}|".format(currentTemp,
                                                 currentHumidity,
                                                 currentWindSpeed,
                                                 currentVisibility))
    print(remindString)


def main():
    # Get input arguments
    args = getOptions()
    api_token = args.token

    # Request type selection
    requestType = ""
    if (args.zip is not None):
        requestType = "zip={},{}".format(args.zip[0], args.zip[1])

    if (args.coord is not None):
        requestType = "lat={}&lon={}".format(args.coord[0], args.coord[1])

    if (args.name is not None):
        requestType = "q={},{}".format(args.name[0], args.name[1])

    if (args.id is not None):
        requestType = "id={}".format(args.id)

    if (requestType == ""):
        print("Error: The request type cannot be empty!")
        print("Check help for options.")
        sys.exit(1)

    unitType = ""
    if (args.unit is not None):
        unitType = args.unit

    api_collector = api_weather.API_Weather(api_token, requestType, unitType)

    # Add reminder in case of snow/rain or too hot weather
    remindString = ""
    if (api_collector.isCold()):
        remindString = "You may need your jacket."
    elif (api_collector.isHot()):
        remindString = "You should cover yourself in shadows."

    # Get json data
    data = api_collector.getJsonData()
    # Call for data printer
    prepareAndPrint(data, remindString, api_collector.tempString,
                    api_collector.windSpeedString)


if __name__ == '__main__':
    main()
