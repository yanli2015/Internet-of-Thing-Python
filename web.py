#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import flask
import subprocess
import datetime
import operator
import json
from flask import Flask, render_template, request, url_for, flash, redirect
from flask import Flask, make_response
import dynamodb
import collections
import operator
from flask import send_file


app = Flask(__name__)
app.secret_key = 'basic_secret'


@app.route('/index.html', methods=['GET'])
def show_customers():
    dynamodb.create_image()
    return render_template('index.html')



if __name__ == "__main__":
    app.run(debug=True, port=80, host='0.0.0.0', threaded=True)
