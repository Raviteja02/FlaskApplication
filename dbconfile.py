from pymongo import MongoClient as mc
import pprint
connection = mc('localhost')
database = connection.studentdb
collection = database.studentinfo
for x in collection.find({'Name':'Raviteja'}):
	print (x['Scno']) 

 