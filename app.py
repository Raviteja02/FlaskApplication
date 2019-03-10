from flask import Flask,render_template,request, session, redirect, url_for,flash
import os
from pymongo import MongoClient as mc
import json
import requests
app=Flask(__name__)
app.secret_key = os.urandom(24)

connection = mc('localhost')
database = connection.PharmacyDB2
collection = database.studentinfo
collection2 = database.ReceivedStock
collection3 = database.AvailableStock
collection4 = database.PharmaReceivedStock
collection5 = database.PharmaAvailableStock


@app.route("/")
def index():
	return render_template("index.html")

@app.route("/AdminLogin")
def AdminLogin():
	return render_template("adminlogin.html")

@app.route("/AdminPage")
def AdminPage():
	return render_template("MainAdminPage.html")


@app.route("/StaffLogin")
def StaffLogin():
	return render_template("stafflogin.html")

@app.route("/StaffPage")
def StaffPage():
	return render_template("staffpage.html")

@app.route("/StudentRegister", methods=['POST','GET'])
def StudentRegister():
	if request.method == 'POST':
		existing_user = collection.find_one({'Admission_number': request.form['Admission_number']})
		if existing_user is None:
			sname = request.form['Student_name']
			admno = request.form['Admission_number']
			fname = request.form['Father_name']
			mname = request.form['Mother_name']
			doj   = request.form['doj']
			doc   = request.form['coursecomplete']
			dept  = request.form['department']
			pwd   = request.form['password']
			sex   = request.form['gender']
			dob   = request.form['dob']
			rel   = request.form['relegion']
			caste = request.form['caste']
			s_caste= request.form['sub_caste']
			course= request.form['course']
			phno  = request.form['contact_no']
			email = request.form['email']
			adno  = request.form['aadhar_no']
			age   = request.form['Age']
			bgp   = request.form['bloodgroup']
			addr  = request.form['address']
			city  = request.form['city']
			Accept = 'False'
			s_data={'Student_name' : sname,'Admission_number' : admno, 'Father_name' : fname, 'Mother_name' : mname, 'doj' : doj,
			'coursecomplete' : doc, 'department' : dept, 'password' : pwd, 'gender' : sex, 'dob' : dob, 'relegion' : rel, 'caste' : caste,
			'sub_caste' : s_caste, 'course' : course, 'contact_no' : phno, 'email' : email, 'aadhar_no' : adno, 'Age' : age,
			'bloodgroup' :bgp, 'address' : addr, 'city' : city,'status':Accept}
			collection.insert_one(s_data)
			session['Admission_number'] = request.form['Admission_number']
			print("data posted Successfully")
			return render_template("submitted.html",sname = sname)
		return render_template("errors.html")
	return render_template("studentreg2.html")



@app.route('/StudentLogin', methods=['POST','GET'])
def Studentlogin():
	if request.method == 'POST':
		login_user = collection.find_one(dict(Admission_number=request.form['Admission_number']))
		print(login_user)
		if login_user:
			if request.form['pass'] == login_user['password']:
				session['Admission_number'] = request.form['Admission_number']
				return redirect(url_for('loggedin'))
		return render_template("studentlogin.html")
	return render_template("studentlogin.html")

@app.route('/LoggedIn')
def loggedin():
    if 'Admission_number' in session:
    	return render_template('logged2.html',name=session['Admission_number'])

    #return 'You are logged in as ' + session['Admission_number']

@app.route('/LoggedOut')
def logout():
	session.pop('Admission_number', None)
	return 'logged out!'

@app.route('/logged2')
def log():
	return render_template("sidebarex.html")


'''Data Posting'''

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





@app.route('/PharmacyStockIssue', methods=['POST','GET'])
def pharmastockissue():
	if request.method == 'POST':
		StockIssueDate = request.form['issue_date']
		TabletName = request.form['tab_name']
		TotalTabsIssued = int(request.form['tabs_qty'])
		RatePerUnit = int(request.form['rate/unit'])
		TotalCost = int(request.form['total_bal'])

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

		return render_template("StockIssued.html")






'''Data Posting Ending'''


'''Data Retreiving'''

@app.route('/VeiwAvailableStock',methods=['POST','GET'])
def viewmainstock():
	if request.method=='GET':
		stockavailable = collection3.find()
		print(stockavailable)
		stockk=[]
		for x in stockavailable:
			stockk.append({"TabletName":x['TabletName'],"TotalTabs":x['TotalTabs'],"RatePerUnit":x['RatePerUnit']})
		print(stockk)
		flash(stockk)
		return render_template('viewmainstock.html')


@app.route('/ViewAllInvoices',methods=['POST','GET'])
def viewinvoices():
	if request.method=='GET':
		invoicedetails = collection2.find()
		invoice=[]
		for x in invoicedetails:
			invoice.append({"InvoiceNumber":x['InvoiceNumber'],"InvoiceDate":x['InvoiceDate'],"StockEntryDate":x['StockEntryDate'],
				"RecievedFrom":x['RecievedFrom'],"TabletName":x['TabletName'],"TotalTabsRecieved":x['TotalTabsRecieved'],
				"RatePerUnit":x['RatePerUnit'],"TotalCost":x['TotalCost'] })
		print(invoice)
		flash(invoice)
		return render_template('invoices.html')

@app.route('/ViewPharmaIssues',methods=['POST','GET'])
def viewpharmaissues():
	if request.method=='GET':
		pharmaissues = collection4.find()
		issues = []
		for x in pharmaissues:
			issues.append({"StockIssueDate":x['StockIssueDate'],"TabletName":x['TabletName'],"TotalTabsIssued":x['TotalTabsIssued'],
				"RatePerUnit":x['RatePerUnit'],"TotalCost":x['TotalCost']})
		flash(issues)
		return render_template('Pharmaissues.html')

@app.route('/ViewPharmaStock',methods=['POST','GET'])
def viewpharmastoc():
	if request.method=='GET':
		pharmastock = collection5.find()
		ph_stock = []
		for x in pharmastock:
			ph_stock.append({"TabletName":x['TabletName'],"TotalTabs":x['TotalTabs'],"RatePerUnit":x['RatePerUnit']})
		flash(ph_stock)
		return render_template('PharmaStock.html')

@app.route('/ViewStudentDetails',methods=['POST','GET'])
def VeiwDetails():
	if request.method=='POST':
		Admno = request.form['Admission_number']
		s_details = collection.find({'Admission_number':Admno})
		st_data=[]
		for x in s_details:
			st_data.append({"Student_name":x['Student_name'],"Admission_number":x['Admission_number'],"Age":x['Age'],
				"gender":x['gender'],"contact_no":x['contact_no']})
		print(st_data)
		flash(st_data)
		return render_template('staffpage.html')

@app.route('/ViewStudentRegistrations')
def ViewStudentRegistrations():
	s_details = collection.find()
	st_data=[]
	for x in s_details:
		st_data.append({"Student_name":x['Student_name'],"Admission_number":x['Admission_number'],"department":x['department'],
			"course":x['course'],"contact_no":x['contact_no'],"email":x['email']})
	flash(st_data)
	return render_template('ViewStudentRegistrations.html')




'''Dtat Retreiving Ending'''

@app.route('/apiconnect',methods=['POST','GET'])
def apicon():
	if request.method=='POST':
		result = request.form
		#x = {'data':result}
		x1 = json.dumps(result)
		print(x1)
		headers = {'content-type': "application/json"}
		url = 'https://9hvrcic270.execute-api.us-east-1.amazonaws.com/records' 
		r = requests.post(url, data = x1, headers= headers)
		print(r.status_code)

	return render_template("firstapi.html")




if __name__ == '__main__':
	app.secret_key = os.urandom(24)
	app.run(debug="True")