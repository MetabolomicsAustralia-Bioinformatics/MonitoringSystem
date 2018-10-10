
# Monitoring System
This is a  Web-based real-time monitoring system to record and visualise the uptime and downtime of instruments.
A administrator module is here for easily manage organisations and isntruments.

The adavantages of this system should be:

1. helps management

2. provides strong evidence in the usage report

3. contributes to instrument error detection

## Run

* run client:
	step 1. update info in config.ini 
	
	step 2. run input/client.py

* run server:
	step 1. bind approritate IP address and port in server_new/server.py
	
	step 2. run server_new/server.py

* run web-app:
	run server_new/app.py

* add admin:
	step 1. open admin.txt, add new admin info in a new line. 
	
	adminname, email, pwd seperated by colon. Eg. admin: admin123@gmail.com: 123
		
	step2. run readAdmin.py
	
## prerequisites

* python 3.6+ installed

* msconverter installed(for client)

http://proteowizard.sourceforge.net/download.html
