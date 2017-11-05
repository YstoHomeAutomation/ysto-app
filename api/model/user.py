#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
from rebel import Database, SqliteDriver
import json, hashlib

class User(object):
    def __init__(self, db):
        driver = SqliteDriver(db)
        self.db = Database(driver)
        
    def all(self):
        _user = self.db.query('select * from Users')
        return json.dumps({u'users': list(_user)})

    def get(self, id):
        _user = self.db.query('select * from Users where id = ?', id)
        return json.dumps({u'users': list(_user)})
        
    def new(self, id, name, password, email):
        _user = self.db.query('select * from Users where id = ?', id)
        
        if _user:
            raise ValueError
        
        password = hashlib.md5(password).hexdigest()
            
        _dev = self.db.execute("""
            insert into Users(id, name, password, email, created_at, updated_at)
            values(:id, :name, :password, :email, (?), (?))
        """, id, name, password, email, datetime.now().strftime('%Y-%m%d %H:%M:%S'), datetime.now().strftime('%Y-%m%d %H:%M:%S'))
            
        return self.get(id)
        
    def update(self, id, name, password, email):
    
        password = hashlib.md5(password).hexdigest()
        
        _user = self.db.execute("""
            update Users
            set name = :name,
                password = :password,
                email = :email,
                updated_at = (?)
            where id = :id
        """, name, password, email, datetime.now().strftime('%Y-%m%d %H:%M:%S'), id)
        
        return self.get(id)
        
    def delete(self, id):
        _user = self.db.query('select * from Users where id = ?', id)
        if _user:
            data = self.get(id)
            _user = self.db.execute('delete from Users where id = ?', id)
        else:
            raise ValueError
        
        return data
        
    def login(self, email, password):
        password = hashlib.md5(password).hexdigest()
        id = self.db.query('select id from Users where email= :email and password= :password', email, password)
        
        return id
        
    def validation(self, auth, auth_value):
        id = auth['id'][0]['id']
        
        if id:
            user = self.db.query('select * from Users where id = (?)', id)
    
        if user: return True
        
        return False
