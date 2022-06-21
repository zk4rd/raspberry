from getmac import get_mac_address
import time
import requests
import json
import sys
import Adafruit_DHT
import time

URL = "https://susano-tech.mn/api/add_data"

def internet_on():
    try:
        res = requests.get('http://google.com', timeout=5)
        return True
    except (requests.ConnectionError, requests.Timeout) as exception:
        return False

def write_file(txt):
        with open('some_datas.txt', 'a') as f:
                f.write(txt + '\n')
                f.close()
def read_file():
        with open('some_datas.txt', 'r') as f:
                lines = f.readlines()
                eth_mac = get_mac_address()
                for line in lines:
                        if "," in line:
                                v = line.split(",")
                                api_call(eth_mac, v[0], v[1], v[2], v[3], v[4],>
                                time.sleep(1)
                f.close()
        return "ok"

def api_call(name,humidity,temperature):
        payload = json.dumps({
            "name": name,
            "temperature": temperature,
            "humidity": humidity
        })
        headers = {
          'Content-Type': 'application/json'
        }
        response = requests.request("POST", URL, headers=headers, data=payload)
        return str(response.text)

while True:
    humidity, temperature = Adafruit_DHT.read_retry(11, 4)

    print('Temp: {0:0.1f} C  Humidity: {1:0.1f} %'.format(temperature, humidity))
					 
    eth_mac = get_mac_address()
    print(eth_mac)
    #result = api_call(eth_mac, str(temperature()), str(humidity()))
    #print(str(result))
    is_online = internet_on()
    if is_online:
     fread = read_file()
     open('some_datas.txt', 'w').close()
     result = api_call(eth_mac, str(temperature()), str(humidity()))
     print(str(result))
    else:
     write_file(str(mpu.temperature())+","+str(humidity()))
    print("-------------------------------")
    time.sleep(600)
