#
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.chrome.service import Service

import os
from time import sleep
import datetime
import pandas as pd
import random


class flight():
    def __init__(self):
        abspath = os.path.abspath('./chromedriver.exe')
        options = webdriver.ChromeOptions()
        service = Service(executable_path=abspath)
        #print(abspath)
        options.add_argument("--lang=en-us")
        options.add_argument('headless') 
        self.browser = webdriver.Chrome(service=service, options=options)
        url = 'https://www.google.com/travel/flights?tfs=CBwQARoaEgoyMDIzLTA3LTAzagwIAhIIL20vMDRqcGxAAUgBcAGCAQsI____________AZgBAg'
        self.browser.get(url)
        self.action = ActionChains(self.browser)
    
    #Initializa of the cookies
    def cookiesPass(self):
        coockiesAccept = self.browser.find_element(By.CSS_SELECTOR,"[class='VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-k8QpJ VfPpkd-LgbsSe-OWXEXe-dgl2Hf nCP5yc AjY5Oe DuMIQc LQeN7 Nc7WLe']")
        self.action.click(coockiesAccept).perform()
    
    #Start position of the flight
    def startPos(self,start):
        startPos = self.browser.find_element(By.XPATH,'/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[1]/div[1]/div/div/div[1]/div/div/input')
        startPos.clear()
        startPos.send_keys(start)
        sleep(1)
        startChoose = self.browser.find_element(By.XPATH,'/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[1]/div[6]/div[3]/ul/li[1]')
        startChoose.click()

    #destination of the flight
    def destination(self,location):
        destination = self.browser.find_element(By.XPATH,'/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[1]/div[4]/div/div/div[1]/div/div/input')
        destination.clear()
        destination.send_keys(location)
        sleep(1)
        destinationChoose = self.browser.find_element(By.XPATH,'/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[1]/div[6]/div[3]/ul/li[1]')
        destinationChoose.click()

    #start date of the flight
    def date(self,startDateValue):
        sleep(1)
        startDate = self.browser.find_element(By.XPATH,'/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[2]/div/div/div[1]/div/div/div[1]/div/div[1]/div/input')
        startDate.click()
        resetDate = self.browser.find_element(By.XPATH,'/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[2]/div/div/div[2]/div/div[2]/div[1]/div[2]/div[2]/button/span')
        resetDate.click()
        startDate.send_keys(startDateValue)
        startDate.send_keys(Keys.TAB)
    
    #search
    def search(self):
        search = self.browser.find_element(By.XPATH,'/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[2]/div')
        search.click()
        sleep(1)
    
    #data decode
    def dataDecoder(self,source):
        sep = source.split(' ')
        output = []
        nextPos = 1
        output.append(sep[nextPos])
        
        nextPos += 2
        output.append(sep[nextPos].split('.')[0])
        
        output.append(sep[nextPos].split('.')[1] != 'This')
        
        if sep[nextPos].split('.')[1] == 'This':
            nextPos += 8
            output.append(sep[nextPos])
        else:
            nextPos += 1
            output.append(sep[nextPos])
        
        if sep[nextPos] == 'Nonstop':
            nextPos += 3
        else:
            nextPos += 4
        start = nextPos
        for i in range(len(sep)-nextPos):
            if sep[i+nextPos] == 'Leaves':
                end=i+nextPos
        temp = ''
        for i in range(end-int(start)):
            temp += sep[start + i] + ' '
        output.append(temp[:-2])
        nextPos = end
        
        pos = []
        for i in range(len(sep)-nextPos):
            if '\u202f' in sep[i+nextPos]:
                pos.append(i+nextPos)
        temp = sep[pos[0]].split('\u202f')
        output.append(temp[0]+temp[1])
        temp = sep[pos[-1]].split('\u202f')
        output.append(temp[0]+temp[1])
        return output

    #get the data
    def getData(self,startPos,destination,flightDate,today):
        #best flights
        sleep(2)
        check = self.browser.find_element(By.XPATH,'/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[2]')
        divcheck = check.find_elements(By.TAG_NAME,'ul')
        if len(divcheck) > 1:
            locate = divcheck[0]
            context = locate.find_elements(By.TAG_NAME,'li')
            data = []
            try:
                for result in context:
                    output = result.find_element(By.XPATH,"./div/div[1]").get_attribute('aria-label')
                    if output != None:
                        storeOutput = self.dataDecoder(output)
                        storeOutput.append(startPos)
                        storeOutput.append(destination)
                        storeOutput.append(flightDate)
                        storeOutput.append(today)
                        data.append(storeOutput)
                        ifFlight = False
            except NoSuchElementException:
                print("No flight exists")
            
            #other flights
            sleep(2)
            #!!!!!!!!!
            locate = divcheck[1]
            context = locate.find_elements(By.TAG_NAME,'li')
            if len(context) > 5:
                expand = context[-1]
                expand.click()
            sleep(2)
            locate = divcheck[1]
            context = locate.find_elements(By.TAG_NAME,'li')
            
            for i in range(len(context)):
                if i != len(context) - 1:
                    result = context[i]
                    try:
                        output = result.find_element(By.XPATH,"./div/div[1]").get_attribute('aria-label')
                    except NoSuchElementException:
                        output = None
                        print("No flight exists")
                    if output != None:
                        storeOutput = self.dataDecoder(output)
                        storeOutput.append(startPos)
                        storeOutput.append(destination)
                        storeOutput.append(flightDate)
                        storeOutput.append(today)
                        data.append(storeOutput)
                #other flights
            if len(data) > 20:
                data = data[:25]
            return data
        else:
            data = []
            return data
    
    #Get date list
    def getDateList(self,start_date):
        period = 150
        
        end_date = ((datetime.datetime.strptime(start_date,'%Y-%m-%d')+datetime.timedelta(days=period)).strftime("%Y-%m-%d"))
        date_list = []
        if isinstance(start_date, str) and isinstance(end_date, str):
            start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
        date_list.append(start_date.strftime('%Y/%m/%d'))
        while start_date < end_date:
            start_date += datetime.timedelta(days=1)
            date_list.append(start_date.strftime('%Y/%m/%d'))
        return date_list
    
    #Get destination list
    def getDestinationList(self):
        df = pd.read_csv('./Airport.csv')
        return df

    def fullProcess(self,startPos,destination,flightDate,today):
        try:
            self.cookiesPass()
            self.startPos(startPos)
            self.destination(destination)
            self.date(flightDate)
            self.search()
            result = self.getData(startPos,destination,flightDate,today)
            self.browser.close()
            return result
        except ElementClickInterceptedException:
            print("Reset date failure")
        
    
model = flight()
# 209 destination
destination = model.getDestinationList()
# date list 
date = '2024-01-16'
dateList = model.getDateList(date)
today = '2024-01-15'
#test
#model.fullProcess('London','Bourgas','2023-10-15',today)

model.browser.close()

name = './record3-2.csv'

priceList = []
unitList = []
luggageList = []
stopList = []
AirlineList = []
startList = []
arriveList = []
startposList = []
destList = []
flightList = []
checkList = []

count = 1
num = 0
dataNum = 50
while num < dataNum:
    print(str(num) + '/' + str(dataNum))
    destPos = random.randint(0,len(destination)-1)
    datetPos = random.randint(0,len(dateList)-1)
    date = dateList[datetPos]
    dest = list(destination['City'])[destPos]
    print(date)
    print(dest)
    model = flight()
    output = model.fullProcess(dest,'London',date,today)
    if output == None:
        output = []
    if len(output) > 0:
        for i in output:
            priceList.append(i[0])
            unitList.append(i[1])
            luggageList.append(i[2])
            stopList.append(i[3])
            AirlineList.append(i[4])
            startList.append(i[5])
            arriveList.append(i[6])
            startposList.append(i[7])
            destList.append(i[8])
            flightList.append(i[9])
            checkList.append(i[10])
    model = flight()
    output = model.fullProcess('London',dest,date,today)
    
    if len(output) > 0:
        for i in output:
            priceList.append(i[0])
            unitList.append(i[1])
            luggageList.append(i[2])
            stopList.append(i[3])
            AirlineList.append(i[4])
            startList.append(i[5])
            arriveList.append(i[6])
            startposList.append(i[7])
            destList.append(i[8])
            flightList.append(i[9])
            checkList.append(i[10])
    num += 1
    
csvFile = {
    'Price':priceList,
    'Unit':unitList,
    'Luggage':luggageList,
    'Stops':stopList,
    'Airline':AirlineList,
    'Depart':startList,
    'Arrive':arriveList,
    'Start':startposList,
    'Destination':destList,
    'FlightDate':flightList,
    'CheckDate':checkList
    }

csvFile = pd.DataFrame(csvFile)
csvFile.to_csv(name)
