from flask import Flask,render_template,request, session, redirect, url_for,flash
from pymongo import MongoClient as mc
from flask_pymongo import PyMongo
import json


connection = mc('localhost')
database = connection.PharmacyDB
collection = database.productinfo

productdetails='''{

"InvoiceNumber":1234,
"InvoiceDate":123456,

"Product1":
{
	"tab_name":"asprin",
	"tabs_rec":"200",
	"rate/unit":"10"
},
"Product2":
{
	"tab_name":"dolo",
	"tabs_rec":"200",
	"rate/unit":"10"
},
"Product3":
{
	"tab_name":"citrazin",
	"tabs_rec":"300",
	"rate/unit":"10"
}

}'''

#it will work if the data is coming in json format

data = request.get_json()

		InvoiceNumber = data['InvoiceNumber']
		InvoiceDate = data['InvoiceDate']
		StockEntryDate = data['StockEntryDate']
		RecievedFrom = data['RecievedFrom']
		for i in data['Products']:
			TabletName = i['tab_name']
			TotalTabsRecieved = int(i['tabs_rec'])
			RatePerUnit = int(i['rate/unit'])
			insert = {'InvoiceNumber' :InvoiceNumber, 'InvoiceDate':InvoiceDate, 'StockEntryDate':StockEntryDate, 'RecievedFrom':RecievedFrom,
			'TabletName':TabletName,'TotalTabsRecieved':TotalTabsRecieved,'RatePerUnit':RatePerUnit,'TotalCost':600}
			collection2.insert_one(insert)
			print('data posted Successfully')

			insert1 = {'TabletName':TabletName, 'TotalTabs':TotalTabsRecieved, 'RatePerUnit':RatePerUnit}

			for x in collection3.find({'TabletName':TabletName}):
				print(x['TabletName'])
				if x['TabletName'] ==TabletName:
					existingTabs=x['TotalTabs']
					tabs = existingTabs+TotalTabsRecieved
					collection3.update_one({'TabletName':TabletName},{'$set': {'TotalTabs':tabs}})

			if collection3.count_documents({'TabletName':TabletName})==0:
				print('hello')
				collection3.insert_one(insert1)

		return 'data success'

#code end!!!

data = json.loads(productdetails)


for product in data['Products']:
	print(product)

print(len(data['Products']))

print(data['Products'][0])

@app.route('/MainStockEntry', methods=['POST','GET'])
def StockEntry():
	TabletName=[]
	TotalTabsRecieved=[]
	RatePerUnit=[]
	if request.method=='POST':
		InvoiceNumber = request.form['invoice_number']
		InvoiceDate = request.form['invoice_date']
		StockEntryDate = request.form['entry_date']
		RecievedFrom = request.form['recieved_from']

		TabletName = request.form['tab_name']
		TotalTabsRecieved = int(request.form['total_tabs'])
		RatePerUnit = int(request.form['rate/unit'])
		TotalCost = int(request.form['total_bal'])
		insert = {'InvoiceNumber' :InvoiceNumber, 'InvoiceDate':InvoiceDate, 'StockEntryDate':StockEntryDate, 'RecievedFrom':RecievedFrom,
		'TabletName':TabletName,'TotalTabsRecieved':TotalTabsRecieved,'RatePerUnit':RatePerUnit,'TotalCost':TotalCost}
		collection2.insert_one(insert)
		print('data posted Successfully')
		insert1 = {'TabletName':TabletName, 'TotalTabs':TotalTabsRecieved, 'RatePerUnit':RatePerUnit}

		for x in collection3.find({'TabletName':TabletName}):
			print(x['TabletName'])
			if x['TabletName'] ==TabletName:
				existingTabs=x['TotalTabs']
				tabs = existingTabs+TotalTabsRecieved
				collection3.update_one({'TabletName':TabletName},{'$set': {'TotalTabs':tabs}})

		if collection3.count_documents({'TabletName':TabletName})==0:
			print('hello')
			collection3.insert_one(insert1)
		
		return render_template("invoices.html")



		product_data = request.get_json()
	#InvoiceNumber = product_data['InvoiceNumber']
	#InvoiceDate   = product_data['InvoiceDate']
	#items = int(len(product_data['Products']))
	'''i=0
	product1=[]
	while i<items:
		product1.append(product_data['Products'][i]['tab_name'])
		product1.append(product_data['Products'][i]['tabs_rec'])
		product1.append(product_data['Products'][i]['rate/unit'])
		i+=1'''

	'''i=0
	for product in product_data['Products'][i]:
		tab0=product['tab_name']
		print(tab0)'''
	for p,q in product_data.items():
		for a,b in q.items():
			print(a,b)


	return '''<h1> the product data is ,
	invoicenumber {},
	invoicedate {},
	items{},
	</h1>'''.format(InvoiceNumber,InvoiceDate,product1)


	
<!--

     $.ajax({
  type: "POST",
  url: "./addstock",
  data: formData,
  success: function(){
    alert('data posted successfully')
  },
  dataType: "json",
  contentType : "application/json"
});

var formData= $('#AddStockForm').serializeJSON();

       console.log(formData)
-->

<script>
        const xhr = new XMLHttpRequest();
    $('form').submit(function() {

     var formData = $('#Myform').serializeJSON();
     var json = JSON.stringify(formData);
     alert(json)

     

     xhr.open("POST","./addstock",true);
     xhr.send(json);
     
    });

     
   

    </script>

    $(document).ready(function() {
    $('form').submit(function(event) {

     var formData = $('#Myform').serializeJSON();
     var json = JSON.stringify(formData);
     alert(json)

     $.ajax({
             url: '/addstock',
             type: 'POST',
             contentType: 'application/json; charset=utf-8',
             dataType: 'json',
             data: {'data':json,'csrfmiddlewaretoken': '{{csrf_token}}'},
             success: function(){
             alert('data posted successfully')
            },
            });
     event.preventDefault();

    });

    });


    <script>
    
    $(document).ready(function() {
    $('form').submit(function(event) {
     var formData = $('#Myform').serializeJSON();
     alert(formData);
     var productdetalis = JSON.stringify(formData);
     alert(productdetalis);

    $.ajax({
             url: '/addstock',
             type: 'POST',
             contentType: 'application/json; charset=utf-8',
             dataType: 'json',
             data: {'data':productdetalis,'csrfmiddlewaretoken': '{{csrf_token}}'},
             success: function(){
             alert('data posted successfully')
            },
            });
     event.preventDefault();

    });

    });
   

    </script>



    @app.route('/MainStockEntry', methods=['POST','GET'])
def StockEntry():
	if request.method=='POST':
		InvoiceNumber = request.form['invoice_number']
		InvoiceDate = request.form['invoice_date']
		StockEntryDate = request.form['entry_date']
		RecievedFrom = request.form['recieved_from']
		TabletName = request.form['tab_name']
		TotalTabsRecieved = int(request.form['total_tabs'])
		RatePerUnit = int(request.form['rate/unit'])
		TotalCost = int(request.form['total_bal'])
		insert = {'InvoiceNumber' :InvoiceNumber, 'InvoiceDate':InvoiceDate, 'StockEntryDate':StockEntryDate, 'RecievedFrom':RecievedFrom,
		'TabletName':TabletName,'TotalTabsRecieved':TotalTabsRecieved,'RatePerUnit':RatePerUnit,'TotalCost':TotalCost}
		collection2.insert_one(insert)
		print('data posted Successfully')
		insert1 = {'TabletName':TabletName, 'TotalTabs':TotalTabsRecieved, 'RatePerUnit':RatePerUnit}

		for x in collection3.find({'TabletName':TabletName}):
			print(x['TabletName'])
			if x['TabletName'] ==TabletName:
				existingTabs=x['TotalTabs']
				tabs = existingTabs+TotalTabsRecieved
				collection3.update_one({'TabletName':TabletName},{'$set': {'TotalTabs':tabs}})

		if collection3.count_documents({'TabletName':TabletName})==0:
			print('hello')
			collection3.insert_one(insert1)
		
		return render_template("invoices.html")