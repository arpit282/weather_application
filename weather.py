from flask import Flask,render_template,url_for,request,jsonify
from flask_cors import cross_origin
import pandas as pd
import pickle
import numpy as np
import pyowm
import random


app = Flask(__name__)
model = pickle.load(open("vot_class.pkl", "rb"))



@app.route("/",methods=['GET'])
@cross_origin()
def home():
	return render_template("index.html")


@app.route("/predict",methods=['GET', 'POST'])
@cross_origin()
def predict():
	if request.method == "POST":
		# DATE

		owm = pyowm.OWM('31db05a57452aedcc0d35d0a1a639a9d')
		mgr = owm.weather_manager()

		date = request.form['date']
		day = float(pd.to_datetime(date, format="%Y-%m-%dT").day)
		month = float(pd.to_datetime(date, format="%Y-%m-%dT").month)

		city_name = str(request.form['cityname'])


		observation = mgr.weather_at_place(city_name)
		w = observation.weather
		temperature = w.temperature('celsius')
		temp =temperature['temp']
		# status = w.detailed_status
		humidity = float(w.humidity)
		wind = w.wind()
		wind_speed = float(wind['speed'])
		wind_degree = float(wind['deg'])
		press = w.pressure
		pressure = float(press['press'])
		if press['sea_level'] is None:
			sea_level = random.choice( [1000,1001,1002,1003,1004,1005,1006,1007,1008,1009,1010,1011,1012,1013,1014,1024,1023])
		else:
			sea_level = float(press['sea_level'])
		clouds = float(w.clouds)
		level = w.barometric_pressure()
		grnd_level= float(level['press'])
		reg = owm.city_id_registry()
		list_of_locations = reg.locations_for(city_name)
		delhi = list_of_locations[0]
		latitude = float(delhi.lat)
		longitude = float(delhi.lon)

		if city_name == 'Delhi' or city_name== 'delhi' or city_name=='DELHI':
			city = float(1)
		elif city_name == 'Hyderabad' or city_name== 'hyderabad' or city_name=='HYDERABAD':
			city = float(2)
		elif city_name == 'Mumbai' or city_name== 'delhi' or city_name=='DELHI':
			city = float(3)
		else:
			city = float(4)


		input_lst = [[city, latitude, longitude, temp, pressure, sea_level, grnd_level, humidity, clouds, wind_speed,wind_degree, month, day]]
		input_lst = np.array(input_lst).reshape((1, -1))
		pred = model.predict(input_lst)

		output = pred
		if output == 0 and (month == 2 or month==1 or month==11 or month==12):
			return render_template("after_sunny.html",city=city_name,pressure = pressure,humidity=humidity,clouds=clouds,day=date, sentense = 'So enjoy the warm sun in this winter season!')
		elif output == 0 and (month == 3 or month==4 or month==4 or month==6 or month==7 or month==8 or month==9 or month==10 ):
			return render_template("after_sunny.html", city=city_name, pressure=pressure, humidity=humidity, clouds=clouds, day=date, sentense='So enjoy yourselves with a cool milkshake and icecream!')
		else:
			return render_template("after_rainy.html",city=city_name,pressure = pressure,humidity=humidity,clouds=clouds,day=date)
	return render_template("index.html")

if __name__=='__main__':
	app.run(debug=True)



