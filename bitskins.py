import requests, json
from datetime import datetime, timedelta

class Item:
	def __init__(self, item):
		withdrawable_at= item['withdrawable_at']
		price= float(item['price'])
		self.available_in= withdrawable_at- datetime.timestamp(datetime.now())
		if self.available_in< 0:
			self.available= True
		else:
			self.available= False
		self.suggested_price= float(item['suggested_price'])
		self.price= price
		self.margin= round(self.suggested_price- self.price, 2)
		self.reduction= round((1- (self.price/self.suggested_price))*100, 2)
		self.image= item['image']
		self.name= item['market_hash_name']
		self.item_id= item['item_id']

	def __str__(self):
		if self.available:
			return "Name: {}\nPrice: {}\nSuggested Price: {}\nReduction: {}%\nAvailable Now!\nLink: https://bitskins.com/view_item?app_id=730&item_id={}".format(self.name, self.price, self.suggested_price, self.reduction, self.item_id)
		else:
			return "Name: {}\nPrice: {}\nSuggested Price: {}\nReduction: {}%\nAvailable in: {}\nLink: https://bitskins.com/view_item?app_id=730&item_id={}".format(self.name, self.price, self.suggested_price, self.reduction, str(timedelta(seconds= self.available_in)), self.item_id)

	def __lt__(self, other):
		return self.reduction < other.reduction
	def __gt__(self, other):
		return self.reduction > other.reduction


def get_url(API_KEY, code):
	PER_PAGE= 30 # the number of items to retrieve. Either 30 or 480.
	return "https://bitskins.com/api/v1/get_inventory_on_sale/?api_key="+ API_KEY+"&code=" + code + "&per_page="+ str(PER_PAGE)

def get_data(url):
	r= requests.get(url)
	data= r.json()
	return data

def get_items(code, API_KEY):
	url= get_url(API_KEY, code)
	try:
		data= get_data(url)
		if data['status']=="success":
			items= []
			items_dic= data['data']['items']
			for item in items_dic:
				tmp= Item(item)
				if tmp.reduction>=25 and tmp.price<=200:	# Minimum discount and maximum price to look for when grabbing items. Currently set at minimum discount of 25% and maxmimum price of $200.
					items.append(tmp)
			return items
		else:
			raise Exception(data["data"]["error_message"])
	except:
		raise Exception("Couldn't connect to BitSkins.")
# my_token = pyotp.TOTP(my_secret)
# print(my_token.now()) # in python3