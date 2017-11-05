#!/usr/bin/env python
# -*- coding: utf-8 -*-

import bottle
from bottle import request, response, install, HTTPError
from bottle import get, post, delete, put, route
from bottle_rest import json_to_params
from bottlejwt import JwtPlugin

from model import device
from model import user

apy = bottle.Bottle()

dev = device.Device('ysto.db')
u = user.User('ysto.db')

install(JwtPlugin(u.validation, 'secret', algorithm='HS256'))

@apy.get('/')
def about():
    response.headers['Content-Type'] = 'application/json'
    response.headers['Cache-Control'] = 'no-cache'

    return {'about': 'ysto-API', 'versao': '2.0.0'}

@apy.get('/devices', auth=1)
def devices():
    response.headers['Content-Type'] = 'application/json'
    response.headers['Cache-Control'] = 'no-cache'

    return dev.all()
    
@apy.get('/devices/<id>', auth=1)
def devices(id):
    response.headers['Content-Type'] = 'application/json'
    response.headers['Cache-Control'] = 'no-cache'

    return dev.get(id)
    
@apy.post('/devices', auth=1)
@json_to_params
def create_device(id, description, switch_on, on_line, user_id):
    try:
        data = dev.new(id, description, switch_on, on_line, user_id)
    except:
        raise HTTPError(400, "'somevar' parameter is required!")
    
    return data
    
@apy.post('/devices/<id>', auth=1)
@json_to_params
def update_device(id, description, switch_on, on_line):
    return dev.update(id, description, switch_on, on_line)
    
@apy.put('/devices/<id>', auth=1)
@json_to_params
def device_switch(id, switch_on):
    return dev.turn_on(id, switch_on)

    
@apy.delete('/devices/<id>', auth=1)
def delete_device(id):
    return dev.delete(id)

@apy.get('/users', auth=1)
def users():
    response.headers['Content-Type'] = 'application/json'
    response.headers['Cache-Control'] = 'no-cache'
    
    return u.all()
    
@apy.get('/users/<id>', auth=1)
def users(id):
    response.headers['Content-Type'] = 'application/json'
    response.headers['Cache-Control'] = 'no-cache'

    return u.get(id)

@apy.post('/users', auth=1)
@json_to_params
def create_user(id, name, password, email):
    try:
        data = u.new(id, name, password, email)
    except:
        raise HTTPError(400, "SOMEVAR parameter is required!")
    
    return data
    
@apy.post('/users/<id>', auth=1)
@json_to_params
def update_user(id, name, password, email):
    return u.update(id, name, password, email)
    
@apy.delete('/users/<id>', auth=1)
def delete_user(id):
    return u.delete(id)
    
@apy.route('/auth', method='POST')
@json_to_params
def login(email, password):
    response.headers['Content-Type'] = 'application/json'
    response.headers['Cache-Control'] = 'no-cache'
    
    id = u.login(email, password)
    if id:
        return JwtPlugin.encode({'id': id})
    else:
        raise HTTPError(401)
