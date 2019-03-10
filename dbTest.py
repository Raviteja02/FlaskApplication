
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
TabletName = '45'
TotalTabsRecieved = 50
RatePerUnit = 55

insert = {'InvoiceNumber' :InvoiceNumber, 'InvoiceDate':InvoiceDate, 'StockEntryDate':StockEntryDate, 'RecievedFrom':RecievedFrom,'TabletName':TabletName,'TotalTabsRecieved':TotalTabsRecieved,'RatePerUnit':RatePerUnit,'TotalCost':(TotalTabsRecieved*RatePerUnit)}
collection2.insert_one(insert)

for x in collection3.find({'TabletName':TabletName}):
	if x['TotalTabsRecieved'] == 0:
		existingTabs = 0	
	else :
		existingTabs = x['TotalTabsRecieved']
	tabs = existingTabs+TotalTabsRecieved
	collection3.update_one({'TabletName':TabletName},{'TotalTabsRecieved':tabs})
