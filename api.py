#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bottle import Bottle, static_file, run

from bottle import request, response, install, HTTPError
from bottle import get, post, delete, put, route
from bottle_rest import json_to_params
from bottlejwt import JwtPlugin

from model import device
from model import user

dev = device.Device('ysto.db')
u = user.User('ysto.db')

install(JwtPlugin(u.validation, 'secret', algorithm='HS256'))

app = Bottle()

@app.get('/api')
def about():
    """ Return a API name and version"""
    response.headers['Content-Type'] = 'application/json'
    response.headers['Cache-Control'] = 'no-cache'
    response.headers['Access-Control-Request-Method'] = '*'

    return {'about': 'ysto-API', 'versao': '2.0.0'}

@app.post('/api/auth')
@json_to_params
def login(email, password):
    """ Return a JWT token, to use in authentication process"""
    response.headers['Content-Type'] = 'application/json'
    response.headers['Cache-Control'] = 'no-cache'
    
    id = u.login(email, password)
    if id:
        return JwtPlugin.encode({'id': id})
    else:
        raise HTTPError(401)

@app.get('/api/devices', auth=1)
def devices():
    """ Return all devices from database"""
    response.headers['Content-Type'] = 'application/json'
    response.headers['Cache-Control'] = 'no-cache'

    return dev.all()
    
@app.get('/api/devices/<id>', auth=1)
def devices(id):
    """ Return a specyfic device by your ID"""
    response.headers['Content-Type'] = 'application/json'
    response.headers['Cache-Control'] = 'no-cache'

    return dev.get(id)
    
@app.post('/api/devices', auth=1)
@json_to_params
def create_device(id, description, switch_on, on_line, user_id):
    """ Create a device by ID"""
    try:
        data = dev.new(id, description, switch_on, on_line, user_id)
    except:
        raise HTTPError(400, "'somevar' parameter is required!")
    
    return data
    
@app.post('/api/devices/<id>', auth=1)
@json_to_params
def update_device(id, description, switch_on, on_line):
    """ Update a device by ID"""
    return dev.update(id, description, switch_on, on_line)
    
@app.put('/api/devices/<id>', auth=1)
@json_to_params
def device_switch(id, switch_on):
    """ Update the state of device by ID"""
    return dev.turn_on(id, switch_on)

    
@app.delete('/api/devices/<id>', auth=1)
def delete_device(id):
    """ Delete a device by ID"""
    return dev.delete(id)

@app.get('/api/users', auth=1)
def users():
    """ Return ALL users from database"""
    response.headers['Content-Type'] = 'application/json'
    response.headers['Cache-Control'] = 'no-cache'
    
    return u.all()
    
@app.get('/api/users/<id>', auth=1)
def users(id):
    """ Return a user by ID"""
    response.headers['Content-Type'] = 'application/json'
    response.headers['Cache-Control'] = 'no-cache'

    return u.get(id)

@app.post('/api/users', auth=1)
@json_to_params
def create_user(name, password, email):
    """ Create new user"""
    try:
        data = u.new(name, password, email)
    except:
        raise HTTPError(400, "SOMEVAR parameter is required!")
    
    #~ return 200
    
@app.post('/api/users/<id>', auth=1)
@json_to_params
def update_user(id, name, password, email):
    """ Update a user by ID"""
    return u.update(id, name, password, email)
    
@app.delete('/api/users/<id>', auth=1)
def delete_user(id):
    """ Delete a user by ID"""
    return u.delete(id)

@app.get('/static/<filepath:path>')
def server_static(filepath):
    """ Define a specific route to find static files to UI"""
    return static_file(filepath, root='ui/static/')

@app.get('/')
def home():
    """ Define a route to find the enter point of this app"""
    return static_file('index.html', root='ui/views/')

if __name__ == '__main__':
    #~ run(app, host='0.0.0.0', port=3001, debug=True)
    run(app, host='192.168.10.101', port=3001)
