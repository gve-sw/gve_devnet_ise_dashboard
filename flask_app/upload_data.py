#!/usr/bin/env python3
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
import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext
import requests
import os
import json
from dotenv import load_dotenv
import datetime


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


# This function runs when you enter the command flask init-data
def init_data():
    db = get_db()

    load_dotenv()
    base_url = "https://" + os.getenv("ISE_IP") + ":9060/ers/config"
    user = os.getenv("ISE_USER")
    password = os.getenv("ISE_PASSWORD")

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    get_all_endpoint = "/endpoint"
    get_all_response = requests.get(base_url+get_all_endpoint, headers=headers, auth=(user, password), verify=False)
    endpoints_response = json.loads(get_all_response.text)["SearchResult"]["resources"]

    for item in endpoints_response:
        detail_response = requests.get(item["link"]["href"], headers=headers, auth=(user, password), verify=False)
        details = json.loads(detail_response.text)["ERSEndPoint"]
        endpoint_id = details["id"]
        name = details["name"]
        mac = details["mac"]
        register_date = datetime.datetime.now()
        category = ""
        if "description" in details:
            description = details["description"]
        else:
            description = ""

        db.execute('INSERT INTO endpoint (id, username, name, description, mac, category, register_date) VALUES (?, ?, ?, ?, ?, ?, ?)',
            (endpoint_id, "n/a", name, description, mac, category, register_date)
        )
        db.commit()

    endpoints = db.execute("SELECT mac FROM endpoint").fetchall()
    for endpoint in endpoints:
        print(endpoint["mac"])


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_data_command)


@click.command('init-data')
@with_appcontext
def init_data_command():
    init_data()
    click.echo('Initialized the data')
