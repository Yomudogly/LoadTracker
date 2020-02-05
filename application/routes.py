from application import app, db, api
from flask import render_template, request, Response, json, jsonify, flash, redirect, url_for, session
import datetime
import time
from application.models import Fullfilment_center, Company, Van, Schedule_wave, Activity
from application.forms import LoginForm
from application.utils import encoder
from flask_restplus import Resource, abort
from flask_jwt_simple import jwt_required, create_jwt, get_jwt_identity



##### API ENDPOINTS #####

##### FULLFILMENT CENTER #####

@api.route('/fc')
class FcGetAndPost(Resource):
    
    # GET ALL
    @jwt_required
    def get(self):
        return jsonify(Fullfilment_center.objects.all())
    
    # POST
    @jwt_required
    def post(self):
        data = api.payload
        fc = Fullfilment_center(fc_name=data['fc_name'], fc_address=data['fc_address'], fc_city=data['fc_city'], fc_zip=data['fc_zip'])
        data['fc_id'] = time.time()
        fc.fc_id = int(data['fc_id'])
        fc.save()
        return jsonify(Fullfilment_center.objects(fc_id=fc.fc_id))

    
@api.route('/fc/<int:idx>')
class FcGetUpdateDelete(Resource):
    
    # GET ONE
    @jwt_required
    def get(self, idx: int):
        return jsonify(Fullfilment_center.objects(fc_id=idx))
    
    # PUT
    @jwt_required
    def put(self, idx: int):
        data = api.payload
        fc = Company(fc_name=data['fc_name'], fc_address=data['fc_address'], fc_city=data['fc_city'], fc_zip=data['fc_zip'])
        Fullfilment_center.objects(fc_id=idx).update(fc_name=fc.fc_name, fc_address=fc.fc_address, fc_city=fc.fc_city, fc_zip=fc.fc_zip)
        return jsonify(Fullfilment_center.objects(fc_id=idx))
    
    # DELETE
    @jwt_required
    def delete(self, idx):
        Fullfilment_center.objects(fc_id=idx).delete()
        return jsonify( message='Fullfilment Center was successfully deleted!')
    
    
###### COMPANY #####

@api.route('/company')
class CompanyGetAndPost(Resource):
    
    # GET ALL
    @jwt_required
    def get(self):
        return jsonify(Company.objects.all())
    
    # POST
    @jwt_required
    def post(self):
        data = api.payload
        company = Company(fc_id=data['fc_id'], company_name=data['company_name'], email=data['email'])
        data['company_id'] = time.time()
        company.company_id = int(data['company_id'])
        company.set_password(data['password'])
        company.save() 
        return jsonify(Company.objects(company_id=company.company_id))
        

@api.route('/company/<int:idx>')
class CompanyGetUpdateDelete(Resource):
    
    # GET ONE
    @jwt_required
    def get(self, idx: int):
        return jsonify(Company.objects(company_id=idx))
    
    # PUT
    @jwt_required
    def put(self, idx: int):
        data = api.payload
        company = Company(fc_id=data['fc_id'], company_name=data['company_name'], email=data['email'])
        company.set_password(data['password'])
        Company.objects(company_id=idx).update(company_name=company.company_name, email=company.email, fc_id=company.fc_id, password=company.password)
        return jsonify(Company.objects(company_id=idx))
    
    # DELETE
    @jwt_required
    def delete(self, idx):
        Company.objects(company_id=idx).delete()
        return jsonify( message='User was deleted successfully!')
    

###### LOGIN #####
  
@api.route('/login')
class Login(Resource):
    
    # POST
    def post(self):

        data = api.payload
        email = data['email']
        password = data['password']
        
        company = Company.objects(email=email).first()
        if company and company.get_password(password):
            return {
                'jwt': create_jwt(identity=email),
                'company_id': company.company_id,
                'company_name': company.company_name
            }, 200
        else:
            return jsonify({ "message": "Bad companyname or password" }), 401
    

###### VAN #####

@api.route('/van')
class VanGetAndPost(Resource):
    
    # GET ALL
    @jwt_required
    def get(self):
        return jsonify(Van.objects.all())
    
    # POST
    @jwt_required
    def post(self):
        data = api.payload
        van = Van(company_id=data['company_id'], vin=data['vin'])
        data['van_id'] = time.time()
        van.van_id = int(data['van_id'])
        van.save() 
        return jsonify(Van.objects(van_id=van.van_id))
    

@api.route('/van/<int:idx>')
class VanGetDelete(Resource):
    
    # GET ONE
    @jwt_required
    def get(self, idx: int):
        return jsonify(Van.objects(van_id=idx))
    
    # DELETE
    @jwt_required
    def delete(self, idx):
        Van.objects(van_id=idx).delete()
        return jsonify( message='Van was successfully deleted!')
    
    
###### SCHEDULE WAVE #####

@api.route('/wave')
class WaveGetAndPost(Resource):
    
    # GET ALL
    @jwt_required
    def get(self):
        return jsonify(Schedule_wave.objects.all())
    
    # POST
    @jwt_required
    def post(self):
        data = api.payload 
        wave = Schedule_wave(company_id=data['company_id'], start_time=data['start_time'], end_time=data['end_time'], status=data['status'])
        data['wave_id'] = time.time()
        wave.wave_id = int(data['wave_id'])
        wave.save()
        return jsonify(Schedule_wave.objects(wave_id=wave.wave_id))
        # ???  how to specify input of DateTimeField ????
        # "start_time": "2020-01-1 20:09:44"
        

@api.route('/wave/<int:idx>')
class WaveGetUpdateDelete(Resource):
    
    # GET ONE
    @jwt_required
    def get(self, idx: int):
        return jsonify(Schedule_wave.objects(wave_id=idx))
    
    # PUT
    @jwt_required
    def put(self, idx: int):
        data = api.payload
        wave = Schedule_wave(company_id=data['company_id'], start_time=data['start_time'], end_time=data['end_time'], status=data['status'])
        Schedule_wave.objects(wave_id=idx).update(company_id=wave.company_id, start_time=wave.start_time, end_time=wave.end_time, status=wave.status)
        return jsonify(Schedule_wave.objects(wave_id=idx))
    
    # DELETE
    @jwt_required
    def delete(self, idx):
        Schedule_wave.objects(wave_id=idx).delete()
        return jsonify( message='Wave was successfully deleted!')


###### ACTIVITY #####

@api.route('/activity')
class ActGetAndPost(Resource):
    
    # GET ALL
    @jwt_required
    def get(self):
        return jsonify(Activity.objects.all())
    
    # POST
    @jwt_required
    def post(self):
        data = api.payload 
        activity = Activity(van_id=data['van_id'], wave_id=data['wave_id'])
        data['act_id'] = time.time()
        activity.act_id = int(data['act_id'])
        activity.save()
        return jsonify(Activity.objects(act_id=activity.act_id))
        # ???  how to specify input of DateTimeField ????
        # "start_time": "2020-01-1 20:09:44"
          

@api.route('/activity/<int:idx>')
class ActGetDelete(Resource):
    
    # GET ONE
    @jwt_required
    def get(self, idx: int):
        return jsonify(Activity.objects(act_id=idx))
    
    # DELETE
    @jwt_required
    def delete(self, idx):
        Activity.objects(act_id=idx).delete()
        return jsonify( message='Activity was successfully deleted!')
    
    
#####################   AGGREGATED QUERIES   ###################    
    
    
######  WAVES BY COMPANY ID  #####

@api.route('/comp_wave/<int:idx>', '/comp_wave')
class CompWaveGet(Resource):
    
    # GET ALL BY ID
    @jwt_required
    def get(self, idx=None):
        
        resp = None
        if idx is None:
            resp = Company.objects.aggregate(*[
    {
        '$lookup': {
            'from': 'schedule_wave', 
            'localField': 'company_id', 
            'foreignField': 'company_id', 
            'as': 'waves'
        }
    }, {
        '$unwind': {
            'path': '$waves', 
            'includeArrayIndex': 'index', 
            'preserveNullAndEmptyArrays': False
        }
    }, {
        '$project': {
            '_id': '$$REMOVE',
            'company_id': '$company_id', 
            'company_name': '$company_name', 
            'wave_id': '$waves.wave_id', 
            'wave_status': '$waves.status', 
            'start_time': {
                '$dateToString': {
                    'format': '%Y-%m-%d %H:%M:%S', 
                    'date': '$waves.start_time'
                }
            }, 
            'end_time': {
                '$dateToString': {
                    'format': '%Y-%m-%d %H:%M:%S', 
                    'date': '$waves.end_time'
                }
            }
        }
    }
])
        else:
            resp = Company.objects.aggregate(*[
                { '$match': { 'company_id' : idx } },
                {
                    '$lookup': {
                        'from': 'schedule_wave', 
                        'localField': 'company_id', 
                        'foreignField': 'company_id', 
                        'as': 'waves'
                    }
                }, {
                    '$unwind': {
                        'path': '$waves', 
                        'includeArrayIndex': 'index', 
                        'preserveNullAndEmptyArrays': False
                    }
                }, {
                    '$project': {
                        '_id': '$$REMOVE', 
                        'wave_id': '$waves.wave_id', 
                        'wave_status': '$waves.status', 
                        'start_time': {
                            '$dateToString': {
                                'format': '%Y-%m-%d %H:%M:%S', 
                                'date': '$waves.start_time'
                            }
                        }, 
                        'end_time': {
                            '$dateToString': {
                                'format': '%Y-%m-%d %H:%M:%S', 
                                'date': '$waves.end_time'
                            }
                        }
                    }
                }
            ])
        
        resp_string = encoder.encode(list(resp))
        
        return json.loads(resp_string), 200
    
    
####### VANS BY COMPANY ID ##########
    
@api.route('/comp_van/<int:idx>', '/comp_van')
class CompVanGet(Resource):
    
    # GET ALL BY ID
    @jwt_required
    def get(self, idx=None):
        
        resp = None
        if idx is None:
            resp = Company.objects.aggregate(*[
                {
                    '$lookup': {
                        'from': 'van', 
                        'localField': 'company_id', 
                        'foreignField': 'company_id', 
                        'as': 'vans'
                    }
                }, {
                    '$unwind': {
                        'path': '$vans', 
                        'preserveNullAndEmptyArrays': False
                    }
                }, {
                    '$project': {
                        '_id': '$$REMOVE', 
                        'company_id': '$company_id', 
                        'company_name': '$company_name', 
                        'van_id': '$vans.van_id',
                        'vin': '$vans.vin'
                    }
                }
            ])
        else:
            resp = Company.objects.aggregate(*[
                { '$match': { 'company_id' : idx } },
                {
                    '$lookup': {
                        'from': 'van', 
                        'localField': 'company_id', 
                        'foreignField': 'company_id', 
                        'as': 'vans'
                    }
                }, {
                    '$unwind': {
                        'path': '$vans', 
                        'preserveNullAndEmptyArrays': False
                    }
                }, {
                    '$project': {
                        '_id': '$$REMOVE',  
                        'company_name': '$company_name', 
                        'van_id': '$vans.van_id',  
                        'vin': '$vans.vin'
                    }
                }
            ])
        resp_string = encoder.encode(list(resp))
        return json.loads(resp_string), 200

        

####### ACTIVITY BY VAN ID ##########
    
@api.route('/van_act/<int:idx>', '/van_act')
class VanActGet(Resource):
    
    # GET ALL BY ID
    @jwt_required
    def get(self, idx=None):
        
        resp = None
        if idx is None:
            resp = Van.objects.aggregate(*[
                {
                    '$lookup': {
                        'from': 'activity', 
                        'localField': 'van_id', 
                        'foreignField': 'van_id', 
                        'as': 'activities'
                    }
                }, {
                    '$unwind': {
                        'path': '$activities', 
                        'preserveNullAndEmptyArrays': False
                    }
                }, {
                    '$project': {
                        '_id': '$$REMOVE', 
                        'van_id': '$van_id', 
                        'vin': '$vin', 
                        'company_id': '$company_id',
                        'wave_id': '$activities.wave_id',
                        'scan_time': {
                            '$dateToString': {
                                'format': '%Y-%m-%d %H:%M:%S', 
                                'date': '$activities.scan_time'
                            }
                        }
                        
                    }
                }
            ])
        else:
            resp = Van.objects.aggregate(*[
                { '$match': { 'van_id' : idx } },
                {
                    '$lookup': {
                        'from': 'activity', 
                        'localField': 'van_id', 
                        'foreignField': 'van_id', 
                        'as': 'activities'
                    }
                }, {
                    '$unwind': {
                        'path': '$activities', 
                        'preserveNullAndEmptyArrays': False
                    }
                }, {
                    '$project': {
                        '_id': '$$REMOVE', 
                        'vin': '$vin', 
                        'company_id': '$company_id',
                        'wave_id': '$activities.wave_id',
                        'scan_time': {
                            '$dateToString': {
                                'format': '%Y-%m-%d %H:%M:%S', 
                                'date': '$activities.scan_time'
                            }
                        }
                        
                    }
                }
            ])
        resp_string = encoder.encode(list(resp))
        return json.loads(resp_string), 200


####### ACTIVITY BY WAVE ID ##########
    
@api.route('/wave_act/<int:idx>', '/wave_act')
class WaveActGet(Resource):
    
    # GET ALL BY ID
    @jwt_required
    def get(self, idx=None):
        
        resp = None
        if idx is None:
            resp = Schedule_wave.objects.aggregate(*[
                {
                    '$lookup': {
                        'from': 'activity', 
                        'localField': 'wave_id', 
                        'foreignField': 'wave_id', 
                        'as': 'activities'
                    }
                }, {
                    '$unwind': {
                        'path': '$activities', 
                        'preserveNullAndEmptyArrays': False
                    }
                }, {
                    '$project': {
                        '_id': '$$REMOVE',   
                        'company_id': '$company_id',
                        'wave_status': '$status', 
                        'start_time': {
                            '$dateToString': {
                                'format': '%Y-%m-%d %H:%M:%S', 
                                'date': '$start_time'
                            }
                        }, 
                        'end_time': {
                            '$dateToString': {
                                'format': '%Y-%m-%d %H:%M:%S', 
                                'date': '$end_time'
                            }
                        },
                        'scan_time': {
                            '$dateToString': {
                                'format': '%Y-%m-%d %H:%M:%S', 
                                'date': '$activities.scan_time'
                            }
                        }
                        
                    }
                }
            ])
        else:
            resp = Schedule_wave.objects.aggregate(*[
                { '$match': { 'wave_id' : idx } },
                {
                    '$lookup': {
                        'from': 'activity', 
                        'localField': 'wave_id', 
                        'foreignField': 'wave_id', 
                        'as': 'activities'
                    }
                }, {
                    '$unwind': {
                        'path': '$activities', 
                        'preserveNullAndEmptyArrays': False
                    }
                }, {
                    '$project': {
                        '_id': '$$REMOVE',   
                        'company_id': '$company_id',
                        'wave_status': '$status', 
                        'start_time': {
                            '$dateToString': {
                                'format': '%Y-%m-%d %H:%M:%S', 
                                'date': '$start_time'
                            }
                        }, 
                        'end_time': {
                            '$dateToString': {
                                'format': '%Y-%m-%d %H:%M:%S', 
                                'date': '$end_time'
                            }
                        },
                        'scan_time': {
                            '$dateToString': {
                                'format': '%Y-%m-%d %H:%M:%S', 
                                'date': '$activities.scan_time'
                            }
                        }
                        
                    }
                }
            ])
        resp_string = encoder.encode(list(resp))
        return json.loads(resp_string), 200


####### ACTIVITY BY COMPANY ID ##########


@api.route('/comp_act/<int:idx>', '/comp_act')
class CompActGet(Resource):
    
    # GET ALL BY ID
    @jwt_required
    def get(self, idx=None):
        
        resp = None
        if idx is None:
            resp = Company.objects.aggregate(*[
                {
                    '$lookup': {
                        'from': 'van', 
                        'localField': 'company_id', 
                        'foreignField': 'company_id', 
                        'as': 'vans'
                    }
                }, {
                    '$unwind': {
                        'path': '$vans', 
                        'includeArrayIndex': 'index', 
                        'preserveNullAndEmptyArrays': False
                    }
                }, {
                    '$project': {
                        '_id': '$$REMOVE', 
                        'company_id': '$company_id', 
                        'company_name': '$company_name', 
                        'van_id': '$vans.van_id', 
                        'vin': '$vans.vin'
                    }
                }, {
                    '$lookup': {
                        'from': 'activity', 
                        'localField': 'van_id', 
                        'foreignField': 'van_id', 
                        'as': 'activities'
                    }
                }, {
                    '$unwind': {
                        'path': '$activities', 
                        'preserveNullAndEmptyArrays': False
                    }
                }, {
                    '$project': {
                        'company_id': '$company_id', 
                        'company_name': '$company_name', 
                        'van_id': '$van_id', 
                        'vin': '$vin', 
                        'wave_id': '$activities.wave_id', 
                        'scan_time': {
                            '$dateToString': {
                                'format': '%Y-%m-%d %H:%M:%S', 
                                'date': '$activities.scan_time'
                            }
                        }
                    }
                }
            ])
        else:
            resp = Company.objects.aggregate(*[
                { '$match': { 'company_id' : idx } },
                {
                    '$lookup': {
                        'from': 'van', 
                        'localField': 'company_id', 
                        'foreignField': 'company_id', 
                        'as': 'vans'
                    }
                }, {
                    '$unwind': {
                        'path': '$vans', 
                        'includeArrayIndex': 'index', 
                        'preserveNullAndEmptyArrays': False
                    }
                }, {
                    '$project': {
                        '_id': '$$REMOVE', 
                        'company_id': '$company_id', 
                        'company_name': '$company_name', 
                        'van_id': '$vans.van_id', 
                        'vin': '$vans.vin'
                    }
                }, {
                    '$lookup': {
                        'from': 'activity', 
                        'localField': 'van_id', 
                        'foreignField': 'van_id', 
                        'as': 'activities'
                    }
                }, {
                    '$unwind': {
                        'path': '$activities', 
                        'preserveNullAndEmptyArrays': False
                    }
                }, {
                    '$project': {
                        'company_name': '$company_name', 
                        'van_id': '$van_id', 
                        'vin': '$vin', 
                        'wave_id': '$activities.wave_id', 
                        'scan_time': {
                            '$dateToString': {
                                'format': '%Y-%m-%d %H:%M:%S', 
                                'date': '$activities.scan_time'
                            }
                        }
                    }
                }
            ])
        resp_string = encoder.encode(list(resp))
        return json.loads(resp_string), 200
    


###### Front End Routes #####

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])

@app.route('/home', methods=['GET', 'POST'])
def index():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        
        company = Company.objects(email=email).first()
        if company and company.get_password(password):
            flash(f'{company.company_name}, you are successfully logged in!', 'success')
            session['company_id'] = company.company_id
            session['company'] = company.company_name
            return redirect(url_for('index'))
        else:
            flash('Wrong Company Name or Password', 'danger')
            
    return render_template('index.html', index=True, form=form)


@app.route('/logout')
def logout():
    session['company_id'] = False
    session.pop('company', None)
    return redirect(url_for('index'))

    