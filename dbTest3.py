
from pymongo import MongoClient as mc

connection = mc('localhost')
database = connection.PharmacyDB2
collection = database.studentinfo
collection2 = database.ReceivedStock
collection3 = database.AvailableStock
collection4 = database.SoldStock

InvoiceNumber = '11'
InvoiceDate = '12'
StockEntryDate = '13'
RecievedFrom = '14'
TabletName = 'lilly'
TotalTabsRecieved = 120
RatePerUnit = 5

insert = {'InvoiceNumber' :InvoiceNumber, 'InvoiceDate':InvoiceDate, 'StockEntryDate':StockEntryDate, 'RecievedFrom':RecievedFrom,'TabletName':TabletName,'TotalTabsRecieved':TotalTabsRecieved,'RatePerUnit':RatePerUnit,'TotalCost':(TotalTabsRecieved*RatePerUnit)}
collection2.insert_one(insert)
insert1 = {'TabletName':TabletName, 'TotalTabs':TotalTabsRecieved, 'RatePerUnit':RatePerUnit}

'''for x in collection3.find({'TabletName':TabletName}):
	print(x['TabletName'])
	if x['TabletName'] ==TabletName:
		existingTabs=x['TotalTabs']
		tabs = existingTabs+TotalTabsRecieved
		collection3.update_one({'TabletName':TabletName},{'$set': {'TotalTabs':tabs}})
	elif collection3.find({'TabletName':TabletName}).count()==0:
		collection3.insert_one(insert1)'''


for x in collection3.find({'TabletName':TabletName}):
	print(x['TabletName'])
	if x['TabletName'] ==TabletName:
		existingTabs=x['TotalTabs']
		tabs = existingTabs+TotalTabsRecieved
		collection3.update_one({'TabletName':TabletName},{'$set': {'TotalTabs':tabs}})

if collection3.count_documents({'TabletName':TabletName})==0:
	print('hello')
	collection3.insert_one(insert1)




		
