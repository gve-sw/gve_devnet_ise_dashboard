""" Copyright (c) 2020 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at
           https://developer.cisco.com/docs/licenses
All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
"""

# Import Section
from flask import Blueprint, flash, g, render_template, request, url_for, redirect
from werkzeug.exceptions import abort
from flask_app.auth import login_required
from flask_app.db import get_db
from collections import defaultdict
import datetime
import requests
import json
from dotenv import load_dotenv
import os
from math import ceil

# load all environment variables
load_dotenv()
BASE_URL = 'https://' + os.getenv('ISE_IP') + ':9060/ers/config'
USER = os.getenv('ISE_USER')
PASSWORD = os.getenv('ISE_PASSWORD')

# set headers for API calls
HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}


# Global variables
bp = Blueprint('portal', __name__)


# Methods
# Returns location and time of accessing device
def getSystemTimeAndLocation():
    # request user ip
    userIPRequest = requests.get('https://get.geojs.io/v1/ip.json')
    userIP = userIPRequest.json()['ip']

    # request geo information based on ip
    geoRequestURL = 'https://get.geojs.io/v1/ip/geo/' + userIP + '.json'
    geoRequest = requests.get(geoRequestURL)
    geoData = geoRequest.json()

    #create info string
    location = geoData['country']
    timezone = geoData['timezone']
    current_time=datetime.datetime.now().strftime("%d %b %Y, %I:%M %p")
    timeAndLocation = "System Information: {}, {} (Timezone: {})".format(location, current_time, timezone)

    return timeAndLocation

#Routes
#Index
@bp.route('/', methods=("GET", "POST"))
@login_required
# This function will render the home page with the registered endpoints table
def index():
    db = get_db()
    if request.method == "POST": # if we're making a post request on this page, we are deleting an endpoint
        delete_endpoint = "/endpoint/{}"
        endpoints_selected = request.form.getlist("endpoint")
        for endpoint in endpoints_selected:
            delete_response = requests.delete(BASE_URL+delete_endpoint.format(endpoint), headers=HEADERS, auth=(USER, PASSWORD), verify=False)

            if delete_response.status_code == 204:
                db.execute("DELETE FROM endpoint WHERE id='{}'".format(endpoint))
                db.commit()
    try:
        #Page without error message and defined header links
        endpoint_select_statement = "SELECT * FROM endpoint"
        endpoints = db.execute(endpoint_select_statement).fetchall()
        total_endpoints = len(endpoints)

        return render_template('portal/index.html', hiddenLinks=False, timeAndLocation=getSystemTimeAndLocation(), endpoints=endpoints, pageTotal=ceil(total_endpoints/20))
    except Exception as e:
        print(e)
        print('There was an issue')
        #OR the following to show error message
        return render_template('portal/index.html', error=False, errormessage="CUSTOMIZE: Add custom message here.", errorcode=e, timeAndLocation=getSystemTimeAndLocation())


#Settings
@bp.route('/add', methods=("GET", "POST"))
@login_required
# This function will render the page to add a new endpoint to the dashboard
def add():
    if request.method == "POST": # if we're making a post request on this page, we have pushed the button to add the endpoint
        db = get_db()

        if request.form.get("mac-addr") != "":
            mac = request.form.get("mac-addr")
            new_endpoint_body = {
                "ERSEndPoint": {
                    "mac": mac
                }
            }

        if request.form.get("name") != "":
            name = request.form.get("name")
            new_endpoint_body["ERSEndPoint"]["name"] = name

        if request.form.get("description") != "":
            description = request.form.get("description")
            new_endpoint_body["ERSEndPoint"]["description"] = description

        if request.form.get("category") != "":
            category = request.form.get("category")

        register_endpoint = "/endpoint/register"
        register_response = requests.put(BASE_URL+register_endpoint,
            headers=HEADERS, auth=(USER, PASSWORD),
            data=json.dumps(new_endpoint_body), verify=False)

        if register_response.status_code == 204:
            get_filter_endpoint = "/endpoint?filter=mac.EQ.{}".format(mac)
            get_endpoint_response = requests.get(BASE_URL+get_filter_endpoint,
                headers=HEADERS, auth=(USER, PASSWORD), verify=False)
            endpoint = json.loads(get_endpoint_response.text)

            db.execute('INSERT INTO endpoint (id, username, name, description, mac, category, register_date) VALUES (?, ?, ?, ?, ?, ?, ?)',
                (endpoint["SearchResult"]["resources"][0]["id"], str(g.user), name, description, mac, category, datetime.datetime.now())
            )
            db.commit()

        return redirect(url_for('portal.index'))

    try:
        #Page without error message and defined header links
        return render_template('portal/add.html', hiddenLinks=False, timeAndLocation=getSystemTimeAndLocation())
    except Exception as e:
        print(e)
        #OR the following to show error message
        return render_template('portal/add.html', error=False, errormessage="CUSTOMIZE: Add custom message here.", errorcode=e, timeAndLocation=getSystemTimeAndLocation())
