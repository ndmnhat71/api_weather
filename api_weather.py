import json
import requests
import sys


class API_Weather:

    def __init__(self, api_token, opt, unit):
        self.api_token = api_token
        self.opt = opt
        self.unit = unit
        self.unitString = unit.lower()

        self.url = "http://api.openweathermap.org/data/2.5/" +\
            "weather?{}&appid={}&units={}".format(opt, api_token, unit)

        if (self.unitString == "metric"):
            self.windSpeedString = "meter/sec"
            self.tempString = '\u00b0C'
        elif (self.unitString == "imperial"):
            self.windSpeedString = "miles/hour"
            self.tempString = '\u00b0F'
        else:
            self.windSpeedString = "meter/sec"
            self.tempString = '\u00b0K'

        self.status = 0
        self.response = self.initializeWeatherData()
        self.jsonData = self.initializeJsonData(self.response)
        try:
            self.validateJsonData(self.jsonData)
        except Exception as error:
            print(error)
            sys.exit(1)

    def initializeWeatherData(self):
        try:
            response = requests.get(self.url, timeout=2)
            # requests.exceptions.Timeout
            self.status = response.status_code
            if (response.status_code != 200):
                raise Exception(
                    "Invalid data returned! Please check api token or option.")
            return response

        except requests.exceptions.RequestException as requestError:
            print(requestError)
            sys.exit(1)

    def initializeJsonData(self, inputData):
        return inputData.json()

    def getJsonData(self):
        return self.jsonData

    def getResposeData(self):
        return self.response

    def validateJsonData(self, jsonData):
        # We can check for invalid values of the json data.
        # This method is called only inside this class.
        dataStatus = True
        if (jsonData['cod'] != 200):
            dataStatus &= False

        if (self.tempString == '\u00b0C' and jsonData['main']['temp'] > 50):
            dataStatus &= False

        if (self.tempString == '\u00b0F' and jsonData['main']['temp'] < -20):
            dataStatus &= False

        if (dataStatus is False):
            raise Exception("Json data is incorrect!")

    def isHot(self):
        if (self.tempString == '\u00b0C' and
                self.jsonData['main']['temp'] > 30):
            return True
        elif (self.tempString == '\u00b0F' and
                self.jsonData['main']['temp'] > 86):
            return True
        else:
            return False

    def isCold(self):
        if (self.tempString == '\u00b0C' and
                self.jsonData['main']['temp'] < 10):
            return True
        elif (self.tempString == '\u00b0F' and
                self.jsonData['main']['temp'] < 50):
            return True
        else:
            return False

    def isRainy(self):
        pass

    def isSnowy(self):
        pass
