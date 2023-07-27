from flask import Flask, redirect, render_template, request, send_file, session, flash, jsonify, Response, url_for ,Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_login import *
from .models import JOB_ADS_database
from . import db

views = Blueprint('views',__name__, template_folder='templates')

@views.route('/')
def index():
    features = JOB_ADS_database.query.all()
    print(features)
    return render_template('index.html',features=features)

@views.route('/recruit')
def recruit():
    return render_template('recruit.html')

@views.route('/view_map')
def view_map():
    file = open('ids.txt', 'r')
    ids=[]
    for i in file.readlines():
        ids.append(int(i))
    file.close()

    print(ids)
    res = []
    for i in ids:
        m = JOB_ADS_database.query.get_or_404(i)
        res.append(m)

    return render_template("map.html",jobs=res)

@views.route('/jobs')
def jobs():
    return render_template('jobs.html')

@views.route('/about_us')
def about_us():
    return render_template('about.html')

@views.route('/cookies')
def cookies():
    return render_template('cookies.html')
    
@views.route('/privacy')
def privacy():
    return render_template('privacy.html')
    
@views.route('/terms')
def terms():
    return render_template('terms.html')

@views.route('/capacity_project')
def capacity_project():
    return render_template('capacity_proj.html')

@views.route('/support')
def support():
    return render_template('support.html')

@views.route('/temp_staff')
def temp_staff():
    return render_template('temp_staff.html')

@views.route('/contact')
def contact():
    return render_template('contact.html')
