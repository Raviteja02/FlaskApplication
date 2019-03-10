@app.route("/addition")
def add(a=10,b=20):
	d = a+b
	return render_template("first.html",display=d)

@app.route("/webform")
def display():
	show = "flask jinji webform"
	return render_template("first.html", display=show)


@app.route("/fileinput")
def input():
	return render_template("fileinput.html")


'''
@app.route('/filewriting', methods=['POST','GET'])
def filewrite():
    a = request.form["i1"]
    b = request.form["i2"]
    c = request.form["i3"]
    print(a)
    print(b)
    print(c)
    x = open("index.txt", "a")
    x.write("My Name is:"+a+"\nMy Number is:"+b+"\nMy Email is:"+c+"\n")
    x.close()
    return render_template('success.html')
'''



@app.route('/filewriting', methods=['POST','GET'])
def insert():
	a = request.form["i1"]
	b = request.form["i2"]
	c = request.form["i3"]
	data = {'Name' : a, 'Sid' : b, 'email' :c }
	collection.insert_one(data)
	print("data posted Successfully")
	return render_template('success.html')


@app.route("/loggeduser")
def display2():
	
	for record in collection.find({'Name':'Raviteja'}):
		name = record["Name"]
		scno = record['Scno']
	return render_template('logged.html',name = name, scno = scno)
			


'''return record['Name']
	return render_template('logged.html',a=record['Name'])'''

 
	
	


