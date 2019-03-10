from pymongo import MongoClient as mc

connection = mc('localhost')
database = connection.PharmacyDB2
collection = database.studentinfo
collection2 = database.ReceivedStock
collection3 = database.AvailableStock
collection4 = database.PharmaReceivedStock
collection5 = database.PharmaAvailableStock


StockIssueDate = 'today'
TabletName = 'Asprin'
TotalTabsIssued = 200
RatePerUnit = 10
TotalCost = 2000






insert = {'StockIssueDate':StockIssueDate, 'TabletName':TabletName, 'TotalTabsIssued':TotalTabsIssued,
		'RatePerUnit':RatePerUnit, 'TotalCost':TotalCost}

for x in collection3.find({'TabletName':TabletName}):
	print(x['TabletName'])
	if x['TabletName'] ==TabletName:
		existingTabs=x['TotalTabs']
		tabs = existingTabs-TotalTabsIssued
		collection3.update_one({'TabletName':TabletName},{'$set': {'TotalTabs':tabs}})

		collection4.insert_one(insert)
		print('data posted Successfully')
insert1 = {'TabletName':TabletName, 'TotalTabs':TotalTabsIssued, 'RatePerUnit':RatePerUnit}

for x in collection5.find({'TabletName':TabletName}):
	print(x['TabletName'])
	if x['TabletName'] ==TabletName:
		existingTabs=x['TotalTabs']
		tabs = existingTabs+TotalTabsIssued
		collection5.update_one({'TabletName':TabletName},{'$set': {'TotalTabs':tabs}})


if collection5.count_documents({'TabletName':TabletName})==0:
	print('hello')
	collection5.insert_one(insert1)