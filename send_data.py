from mpu6050 import mpu6050
from getmac import get_mac_address
import time
import requests
import json
import os
mpu = mpu6050(0x68)
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
				api_call(eth_mac, v[0], v[1], v[2], v[3], v[4], v[5], v[6])
				time.sleep(1)
		f.close()
	return "ok"

def api_call(name,temp,x1,y1,z1,x2,y2,z2):
	payload = json.dumps({
		"name": name,
	    "temperature": temp,
	    "accel_x": x1,
	    "accel_y": y1,
	    "accel_z": z1,
	    "gyro_x": x2,
		"gyro_y": y2,
		"gyro_z": z2
	})
	headers = {
	  'Content-Type': 'application/json'
	}
	response = requests.request("POST", URL, headers=headers, data=payload)
	return str(response.text)

while True:
    print("Temp : "+str(mpu.get_temp()))
    print()

    accel_data = mpu.get_accel_data()
    print("Acc X : "+str(accel_data['x']))
    print("Acc Y : "+str(accel_data['y']))
    print("Acc Z : "+str(accel_data['z']))
    print()

    gyro_data = mpu.get_gyro_data()
    print("Gyro X : "+str(gyro_data['x']))
    print("Gyro Y : "+str(gyro_data['y']))
    print("Gyro Z : "+str(gyro_data['z']))
    print()
	eth_mac = get_mac_address()
	print(eth_mac)
	is_online = internet_on()
	if is_online:
		fread = read_file()
		open('some_datas.txt', 'w').close()
		result = api_call(eth_mac, str(mpu.get_temp()), str(accel_data['x']), str(accel_data['y']), str(accel_data['z']), str(gyro_data['x']), str(gyro_data['y']), str(gyro_data['z']))
		print(str(result))
	else:
		write_file(str(mpu.get_temp())+","+str(accel_data['x'])+","+str(accel_data['y'])+","+str(accel_data['z'])+","+str(gyro_data['x'])+","+str(gyro_data['y'])+","+str(gyro_data['z']))
	print("-------------------------------")
    time.sleep(600)
	
	
	
pm2 start send_data.py --name myApp
pm2 save
sudo pm2 startup systemd -u susanochip1
pm2 resurrect




[Install]
WantedBy=multi-user.target

[Unit]
Description=Example service
Wants=network-online.target
After=network-online.target

[Service]
User=susanochip1
Group=susanochip1
ExecStart=/home/susanochip1/send_data.py
ExecStartPre=/bin/sleep 10
Type=simple

[Timer]
OnStartupSec=25