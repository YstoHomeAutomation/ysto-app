#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from webtest import TestApp
import api
import json

app = TestApp(api.app)

class TestAPI(unittest.TestCase):

    def test_about(self):
        resp=app.get('/api')
        app.reset()
        assert resp.json == {"versao": "2.0.0", "about": "ysto-API"}

    def test_token_ok(self):
        resp = app.post_json('/api/auth', {'email':'fabiano@mail.net', 'password':'123456'})
        token=resp.json
        app.reset()
        assert resp.status_code == 200

    def test_get_devices(self):
        resp = app.get('/api/devices', dict(Authorization='bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6W3siaWQiOjF9XX0.eetLj4DKGNshMe9uCZmtvOayZPFHva_PsrqANvG6pRI'))
        app.reset()
        assert resp.status_code == 200
        
    def test_get_devices_id(self):
        resp = app.get('/api/devices/670', dict(Authorization='bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6W3siaWQiOjF9XX0.eetLj4DKGNshMe9uCZmtvOayZPFHva_PsrqANvG6pRI'))
        device = resp.json['devices']
        app.reset()
        assert resp.status_code == 200
        assert device[0]['description'] == 'MA003'

    def test_get_users(self):
        resp = app.get('/api/users', dict(Authorization='bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6W3siaWQiOjF9XX0.eetLj4DKGNshMe9uCZmtvOayZPFHva_PsrqANvG6pRI'))
        user = resp.json['users']
        app.reset()
        assert resp.status_code == 200
        assert user[0]['name'] == 'Fabiano Gomes'

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestAPI)
    unittest.TextTestRunner(verbosity=2).run(suite)
