#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
from rebel import Database, SqliteDriver
import paho.mqtt.client as mqtt
import json

# TODO: Controle do device via mqqt, na autalização
client = mqtt.Client('central')
client.loop_start()
client.connect('192.168.10.101', port=1883, keepalive=60)

class Device(object):
    def __init__(self, db):
        driver = SqliteDriver(db)
        self.db = Database(driver)

    def all(self):
        _dev = self.db.query('select * from Devices')
        return json.dumps({u'devices': list(_dev)})

    def get(self, id):
        _dev = self.db.query('select * from Devices where id = ?', id)
        return json.dumps({u'devices': list(_dev)})
        
    def new(self, id, description, switch_on, on_line, user_id):
        _dev = self.db.query('select * from Devices where id = ?', id)
        
        if _dev:
            raise ValueError
            
        _dev = self.db.execute("""
            insert into Devices(id, description, switch_on, on_line, created_at, updated_at, user_id)
            values(:id, :description, :switch_on, :on_line, (?), (?), :user_id)
        """, id, description, switch_on, on_line, datetime.now().strftime('%Y-%m%d %H:%M:%S'), datetime.now().strftime('%Y-%m%d %H:%M:%S'), user_id)
            
        return self.get(id)
        
    def update(self, id, description, switch_on, on_line):
        _dev = self.db.execute("""
            update Devices
            set description = :description,
                switch_on = :switch_on,
                on_line = :on_line,
                updated_at = (?)
            where id = :id
        """, description, switch_on, on_line, datetime.now().strftime('%Y-%m%d %H:%M:%S'), id)
        
        return self.get(id)
        
    def turn_on(self, id, switch_on):
        _dev = self.db.query('select description from Devices where id=(?)', id)
        
        if not _dev:
            raise ValueError
            
        topic = _dev[0]['description'] + '/relay'
        
        client.subscribe(topic)
        client.publish(topic, switch_on)
        client.unsubscribe(topic)
    
        _dev = self.db.execute("""
            update Devices
            set switch_on = :switch_on,
                updated_at = (?)
            where id = :id
        """, switch_on, datetime.now().strftime('%Y-%m%d %H:%M:%S'), id)
        
        return self.get(id)
        
    def delete(self, id):
        _dev = self.db.query('select * from Devices where id = ?', id)
        if _dev:
            data = self.get(id)
            _dev = self.db.execute('delete from Devices where id = ?', id)
        else:
            raise ValueError
        
        return data
