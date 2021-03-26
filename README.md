# BEITECH Practical Exercise

### **Step by step installation in Manjaro Linux**

Download the repository and go to the project folder

* cd b_practical_exercise

Create a new virtual environment and activate it:

* python3 -m venv venv
* source venv/bin/activate

Install libraries and check if all files and folders has permission to be executed.

* python3 -m pip install -r requirements.txt
* ls -las

You need to create de database

* python3 db_builder.py

Get the web service up and running

* python3 app.py

To get more info about enpoints you can check this url:
* http://localhost:2222/api/ui

Finally access this URL to list the orders:
* http://localhost:2222


### **Tested with:**

* Python 3.9.2

* SQLite 3.34.1

* Mozilla Firefox 86.0.1 and Google Chrome 88.0.4324.96
