#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bottle import static_file, run

from bottle import request, response, install, HTTPError
from bottle import get, post, delete, put, route
from bottle_rest import json_to_params
from bottlejwt import JwtPlugin

from model import device
from model import user

dev = device.Device('ysto.db')
u = user.User('ysto.db')

install(JwtPlugin(u.validation, 'secret', algorithm='HS256'))

@get('/api')
def about():
    response.headers['Content-Type'] = 'application/json'
    response.headers['Cache-Control'] = 'no-cache'

    return {'about': 'ysto-API', 'versao': '2.0.0'}

@route('/api/auth', method='POST')
@json_to_params
def login(email, password):
    response.headers['Content-Type'] = 'application/json'
    response.headers['Cache-Control'] = 'no-cache'
    
    id = u.login(email, password)
    if id:
        return JwtPlugin.encode({'id': id})
    else:
        raise HTTPError(401)


@get('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='ui/static/')

@get('/')
def home():
    return static_file('index.html', root='ui/views/')

run(host='0.0.0.0', port=3001, debug=True)
