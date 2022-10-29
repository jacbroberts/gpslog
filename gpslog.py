import os
import subprocess
import json
import csv
from datetime import datetime
file_empty = True
filename=datetime.now().strftime('%a-%m-%y-%H-%M-%S')
def log():
	global file_empty
	file_empty = False
	with open(f"log{filename}.csv", mode="a") as cf:
		writer = csv.writer(cf, delimiter=",", quotechar='"',quoting=csv.QUOTE_MINIMAL)
		if file_empty:
			writer.writerow(['time','lat','long','alt','speed'])
		else:
			for i in entries:
				writer.writerow(i)

	entries.clear()

entries = []
while True:
	try:
		gps_cmd = "gpspipe -w -n 4"
		gps_out = subprocess.check_output(gps_cmd, shell=True, stderr=subprocess.STDOUT)
		gps_out = gps_out.decode('utf-8')
		gps_lines = gps_out.split("\r\n")
		for line in gps_lines:
			if "lat" in line:
				data = json.loads(line)
				time = data['time']
				lat = data['lat']
				long = data['lon']
				alt = data['alt']
				speed = data['speed']
				entry = (time,lat,long,alt,speed)
				entries.append(entry)
				print(f"{time}!{lat}!{long}!{alt}!{speed}")
				if len(entries) >= 10:
					log()
				break
	except Exception as e:
		print(e)
		pass
