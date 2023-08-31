from flask import Flask, redirect, render_template, request, send_file, session, flash, jsonify, Response, url_for ,Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_login import *
from faulthandler import disable
from io import BytesIO
from fileinput import filename
from .func import convert_salary
from .models import JOB_ADS_database, REQUESTS_database
from . import db
import json

employees = Blueprint('employees',__name__)

@employees.route('/_autocomplete', methods=['GET'])
def autocomplete():
    locations = JOB_ADS_database.query.all()
    p = []
    for i in locations:
        p.append(i.location)
    p = list(dict.fromkeys(p))
    print(p)
    return Response(json.dumps(p), mimetype='application/json')

@employees.route('/search', methods=['GET','POST'])
def search():
    if request.method == 'POST':
        keywords = request.form.get('keywords')
        occupation = request.form.get('occupation')
        specialty = request.form.get('specialty')
        location = request.form.get('location')
        min_salary = request.form.get('min-salary')
        max_salary = request.form.get('max-salary')
        salary_per = request.form.get('salary_per')
        perm = request.form.get('perm')
        temp = request.form.get('temp')
        full = request.form.get('full')
        part = request.form.get('part')

        simpleform = [keywords,occupation,specialty,location]

        #filter by contract of length
        contractlength = [perm,temp,full,part]
        print("contractlength is: ",contractlength)

        newform = []
        for j in simpleform:
            if j:
                if j!='All':newform.append(j)

        #Serach for all the job adds which match with the filtering options in newform and add them in a list-----------------------------------------------------------------------------
        print("newform is: ",newform)
        if newform:
            m = []
            for i in newform:
                m.append(JOB_ADS_database.query.msearch(str(i),fields=['org_name','reg_staff','location','salary_per','specialty','contract_length','staff_type','position','job_desc']).all())

            print("m is: ",m)

            #find the queries which combine all the search fields
            search_res=[]
            result = set(m[0])
            for s in m[1:]:
                result.intersection_update(s)
            search_res.append(result)

            #find length of correct queries
            l=0
            for i in search_res[0]:l+=1

            #filter by length of contract----------------------------------------------------------------------------------------------------

            #if more than two contract length options remove from the 
            # list the ones that don't include the chosen contract options.
            # So keep the queries with the checked contract options
            c = []
            for i in contractlength:
                if i:
                    if contractlength[0]=="on":c.append('perm')
                    if contractlength[1]=="on":c.append('temp')
                    if contractlength[2]=="on":c.append('full')
                    if contractlength[3]=="on":c.append('part')
            
            c = list(dict.fromkeys(c))
            new_list = []
            if contractlength:
                for i in search_res[0]:
                    for j in c:
                        if j in i.contract_length:
                            new_list.append(i)
                
            if new_list:search_res[0] = set(new_list)

            print("-----------")
            print(search_res[0])

            #filter by salary the above queries----------------------------------------------------------------------------------------------------
            if not max_salary:max_salary = 10000000

            k=0
            res=[]
            result=[]
            #filter by salary (compare everyting with monthly salary)
            if salary_per=='All' and min_salary:
                for j in search_res[0]:
                    job_monthly_salary = convert_salary(j.salary_per,j.salary)
                    min_salary = convert_salary("Monthly",min_salary)
                    max_salary = convert_salary("Monthly",max_salary)
        
                    if float(job_monthly_salary) >= float(min_salary) and float(job_monthly_salary) <= float(max_salary):
                        print(j)
                        k+=1
                        res.append((j))
                        
                result.append(res)
                print("result is: ",result)

                file = open('ids.txt', 'w')
                l = 0
                for i in result[0]:
                    file.write(str(i.id)+'\n')
                    l+=1
                file.close()

                return render_template('search.html',search_res = result, simpleform = newform ,l=l) #k
            
            #filter by salary_per and salary
            res=[]
            result=[]
            k=0
            if salary_per!='All' and min_salary:
                for j in search_res[0]:
                    if j.salary_per == salary_per and float(j.salary) >= float(min_salary) and float(j.salary) <= float(max_salary):
                        print(j)
                        k+=1
                        res.append((j))

                result.append(res)
                print("result is: ",result)

                file = open('ids.txt', 'w')
                l = 0
                for i in result[0]:
                    if i.visibility == 1:
                        file.write(str(i.id)+'\n')
                        l+=1
                file.close()

                return render_template('search.html',search_res = result, simpleform = newform ,l=l) #k

            #filter only by salary_per (day,month,annum, etc)
            temp = []
            if salary_per!='All' and not min_salary and salary_per!=None: 
                for i in search_res[0]:
                    if i.salary_per == salary_per:temp.append([i])

                #fix the format of result
                search_res = []
                for i in temp:search_res.append(i[0])
                search_res = list(search_res)

                result = []
                result.append(search_res)

                
                file = open('ids.txt', 'w')
                l = 0
                if len(search_res) == 0:
                    pass
                else:
                    for i in search_res:
                        if i.visibility == 1:
                            file.write(str(i.id)+'\n')
                            l+=1
                    file.close()

                return render_template('search.html',search_res = result, simpleform = newform ,l=l) 

            
            #-----------------------------------------------------------------------------------------------------------------------------------

            print('search_res is ',search_res)    

            file = open('ids.txt', 'w')
            l=0
            for i in search_res[0]:
                if i.visibility == 1:
                    file.write(str(i.id)+'\n')
                    l+=1
            file.close()

            print(1)
            return render_template('search.html',search_res = search_res, simpleform = newform ,l=l) 

        else:#no input
            m = JOB_ADS_database.query.all()
            search_res=[]
            search_res.append(JOB_ADS_database.query.all())
            l = 0

            file = open('ids.txt', 'w')
            for i in search_res[0]:
                if i.visibility == 1:
                    file.write(str(i.id)+'\n')
                    l+=1
            file.close()

            print(2)
            return render_template('search.html',search_res = search_res, simpleform = simpleform, l=l)
        
@employees.route('/category/<cat>')
def category(cat):
    file = open('ids.txt', 'r')
    ids=[]
    for i in file.readlines():
        ids.append(int(i))
    file.close()

    print(ids)

    res = []
    search_res  =[]
    l=0
    for i in ids:
        m = JOB_ADS_database.query.get_or_404(i)
        res.append(m)
        l+=1

    if cat =="date":
        result = JOB_ADS_database.query.filter(JOB_ADS_database.id.in_(ids)).all()
        result.reverse()
    
    elif cat=="sal_desc":
        #result = JOB_ADS_database.query.filter(JOB_ADS_database.id.in_(ids)).order_by(JOB_ADS_database.salary.desc()).all()
        #result = JOB_ADS_database.query.filter(JOB_ADS_database.id.in_(ids)).order_by(convert_salary(JOB_ADS_database.salary_per,JOB_ADS_database.salary).desc()).all()
        result = JOB_ADS_database.query.filter(JOB_ADS_database.id.in_(ids)).all()
        result = sorted(result , key=lambda x: convert_salary(x.salary_per, x.salary))
        result.reverse()


    elif cat=="sal_asc":
        #result = JOB_ADS_database.query.filter(JOB_ADS_database.id.in_(ids)).order_by(JOB_ADS_database.salary.asc()).all()
        #result = JOB_ADS_database.query.filter(JOB_ADS_database.id.in_(ids)).order_by(convert_salary(JOB_ADS_database.salary_per,JOB_ADS_database.salary).asc()).all()
        result = JOB_ADS_database.query.filter(JOB_ADS_database.id.in_(ids)).all()
        result = sorted(result , key=lambda x: convert_salary(x.salary_per, x.salary))

    else:
        result = res

    search_res.append(result)

    
    return render_template('search.html',search_res=search_res,l=l) 

@employees.route('/_view_map',methods=['GET'])
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

    # Convert the SQLAlchemy objects to a list of dictionaries
    user_data = [{'id': job.id,'staff_type': job.staff_type, 'specialty': job.specialty, 'job_desc': job.job_desc, 'location': job.location} for job in res]
    print(user_data)

    return Response(json.dumps(user_data), mimetype='application/json')
    #return render_template("map.html",jobs=res)


@employees.route('/apply/<int:id>')
def apply(id):
    ad = JOB_ADS_database.query.filter_by(id=id).first()
    print(id)
    return render_template('apply.html',ad=ad)

@employees.route('/download/<string:filename>')
def download(filename):
    upload = JOB_ADS_database.query.filter_by(filename=filename).first()
    print(upload)
    return send_file(BytesIO(upload.data), download_name=upload.filename, as_attachment=True)

@employees.route('/choose/<string:sector>')
def choose(sector):
    features = JOB_ADS_database.query.filter_by(staff_type=sector).all()
    print(features)
    return render_template('index.html',features=features)

@employees.route('/send_app/<int:id>', methods=['POST'])
def send_app(id):
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        phone_number = request.form.get('phone_num')
        file= request.files.get('pdf')
        job_id = int(id)

        ad = REQUESTS_database(first_name=first_name, last_name=last_name, email=email, phone_number = phone_number, job_id = job_id , filename=file.filename,data=file.read())
        db.session.add(ad)
        db.session.commit()
        flash('Request submitted suuccessfully!')
        return redirect('/apply/'+str(id))