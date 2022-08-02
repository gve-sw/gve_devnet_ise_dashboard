# GVE DevNet NetReg ISE Dashboard
This repository contains code to a Flask app that utilizes the Cisco ISE APIs to display registered endpoints onto a web dashboard. The registered endpoints are displayed with their name, MAC address, description, date registered, and endpoint grouping. From the dashboard, it is possible to remove the endpoint from ISE. Additionally, it is possible to add new endpoints to the dashboard and ISE.

## Contacts
* Danielle Stacy

## Solution Components
* [ISE Rest APIs](https://community.cisco.com/t5/security-documents/ise-ers-api-examples/ta-p/3622623#toc-hId--623796905)
* Python 3.9
* Flask
* SQLite


## Prerequisites

#### ISE REST APIs
1. Login to your ISE PAN using the admin or other SuperAdmin user.
2. Navigate to `Administration > System > Settings` and select `ERS Settings` from the left panel.
3. Enable the ERS APIs by selecting **Enable ERS** for Read/Write
4. Do not enable CSRF unless you know how to use the tokens.
5. Select **Save** to save your changes.
6. The following ISE Administrator Groups allow REST API access:
    * SuperAdmin: Read/Write
    * ERSAdmin: Read/Write
    * ERSOperator: Read Only

###### Create REST API Users
You can use the default ISE admin account for ERS APIs since it has SuperAdmin privileges. However, it is recommended to create separate users with the ERS Admin (Read/Write) or ERS Operator (Read-Onlly) privileges to use the ERS APIs so you can separately track and audit their activities.

> Note: the MNT API uses different permissions. If you are going to do MNT and ERS you will need a group with both permissions

1. Navigate to `Administration > System > Admin Access`
2. Choose `Administrators > Admin Users` from the left pane
3. Choose `+Add > Create an Admin User` to create a new ers-admin and ers-operator accounts.

To create any API request from ISE REST APIs section, substitute your encoded credentials in the HTTP Authorization header. Like the example below:

```
authencode = config.api_user+":"+config.api_password
authencode = authencode.encode("ascii")
userAndPass = b64encode(authencode).decode("ascii")
headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Authorization": "Basic %s" % userAndPass
    }
return headers
```


## Installation/Configuration
1. Clone this repository with `git clone https://github.com/gve-sw/gve_devnet_ise_dashboard` and open the directory of the root repository.
2. Set up a Python virtual environment. Make sure Python 3 is installed in your environment, and if not, you may download Python [here](https://www.python.org/downloads/). Once Python 3 is installed in your environment, you can activate the virtual environment with the instructions found [here](https://docs.python.org/3/tutorial/venv.html).
3. Add ISE IP address, username, and password where the API was enabled in the Prerequisites section to the environmental variables in the .env file. 
```python
ISE_IP='ip goes here'
ISE_USER='username goes here'
ISE_PASSWORD='password goes here'
```
4. The flask app is contained in the flask_app directory, so we should let the program know where to check for the app. Set the flask environmental settings with the following commands:
```
$ export FLASK_APP=flask_app
$ export FLASK_ENV=development
```
5. To initialize the database (this is only needed on the first use), use the command:
```
$ flask init-db
```
6. To populate the database with the endpoints currently registered with your ISE environment, use the command:
```
$ flask init-data
```
7. Finally, to start the Flask app, use the command:
```
$ flask run
```


## Usage
As noted previously, the code to run the flask app is located in the flask_app directory. The file portal.py contains the functions that render the home screen and add endpoints. This is also where the delete functionality is defined. The file auth.py contains the functions that render the login and register user screens. The database functionalities are defined in db.py, and the functions to populate the database with endpoints already in the ISE dashboard are found in upload_data.py.


#### Access dashboard
You may access the dashboard by opening the browser of your choice and entering the address 127.0.0.1:5000

#### Log In/Register User
If you are not logged into the dashboard, you will be directed to the login page, where you are prompted to enter a username and password. To register a user, click the Register New User option on the top menu and then register a unique username and password. Once registered, you should be directed to the Login page, where you may login with those credentials.

#### Home page
Once you are logged in, you are able to view the different registered endpoints that have been added to the dashboard and ISE. The table that displays the registered endpoints shows the name, MAC address, description, date registered, and category of the device. From this page, you can also remove an endpoint from the dashboard and from ISE. Simply select the checkbox next to the entries that you wish to delete and then click the Delete button under the table. The page will reload with those endpoints removed, and those endpoints will also be removed from your instance of ISE.

#### Add endpoints
To add an endpoint to the dashboard and register it with ISE, click the Register Endpoint option on the top menu. On this page, you will be prompted to give the name, MAC address, description, and category of the endpoint.

#### Logout
Once you would like to log off of the dashboard, click the logout option in the top right menu. This will log out the user and return you to the login screen.

# Screenshots

![/IMAGES/0image.png](/IMAGES/0image.png)

Login Screen
![/IMAGES/login.png](/IMAGES/login.png)

Register User
![/IMAGES/register_user.png](/IMAGES/register_user.png)

Home Screen
![/IMAGES/home.png](/IMAGES/home.png)

Register Endpoint
![/IMAGES/register_endpoint.png](/IMAGES/register_endpoint.png)

### LICENSE

Provided under Cisco Sample Code License, for details see [LICENSE](LICENSE.md)

### CODE_OF_CONDUCT

Our code of conduct is available [here](CODE_OF_CONDUCT.md)

### CONTRIBUTING

See our contributing guidelines [here](CONTRIBUTING.md)

#### DISCLAIMER:
<b>Please note:</b> This script is meant for demo purposes only. All tools/ scripts in this repo are released for use "AS IS" without any warranties of any kind, including, but not limited to their installation, use, or performance. Any use of these scripts and tools is at your own risk. There is no guarantee that they have been through thorough testing in a comparable environment and we are not responsible for any damage or data loss incurred with their use.
You are responsible for reviewing and testing any scripts you run thoroughly before use in any non-testing environment.
