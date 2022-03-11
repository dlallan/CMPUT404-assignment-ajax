#!/usr/bin/env python
# coding: utf-8
# Copyright 2013 Abram Hindle
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Modifications to source code in this file were made to enhance functionality.
# Copyright 2022 Dillon Allan
#
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version. This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details. You should have received a copy of the GNU Affero General Public License along with this program. If not, see <https://www.gnu.org/licenses />.
#
# You can start this by executing it in python:
# python server.py
#
# remember to:
#     pip install flask


from flask import Flask, jsonify, redirect, request
import json

app = Flask(__name__)
app.debug = True

# An example world
# {
#    'a':{'x':1, 'y':2},
#    'b':{'x':2, 'y':3}
# }


class World:
    def __init__(self):
        self.clear()

    def update(self, entity, key, value):
        entry = self.space.get(entity, dict())
        entry[key] = value
        self.space[entity] = entry

    def set(self, entity, data):
        self.space[entity] = data

    def clear(self):
        self.space = dict()

    def get(self, entity):
        return self.space.get(entity, dict())

    def world(self):
        return self.space

# you can test your webservice from the commandline
# curl -v   -H "Content-Type: application/json" -X PUT http://127.0.0.1:5000/entity/X -d '{"x":1,"y":1}'


myWorld = World()

# I give this to you, this is how you get the raw body/data portion of a post in flask
# this should come with flask but whatever, it's not my project.


def flask_post_json():
    '''Ah the joys of frameworks! They do so much work for you
       that they get in the way of sane operation!'''
    if (request.json != None):
        return request.json
    elif (request.data != None and request.data.decode("utf8") != u''):
        return json.loads(request.data.decode("utf8"))
    else:
        return json.loads(request.form.keys()[0])


@app.route("/")
def hello():
    '''Redirect to /static/index.html'''
    return redirect('/static/index.html')


@app.route("/entity/<entity>", methods=['POST', 'PUT'])
def update(entity):
    '''update the entities via this interface'''
    # if request.mimetype == 'application/json' and request.data:
    #     myWorld.set(entity, request.json)
    #     return jsonify(myWorld.get(entity))
    # return {}
    if not request.data:
        return {}
    myWorld.set(entity, flask_post_json())
    return myWorld.get(entity)


@app.route("/world", methods=['POST', 'GET'])
def world():
    '''you should probably return the world here'''
    return myWorld.world()


@app.route("/entity/<entity>")
def get_entity(entity):
    '''This is the GET version of the entity interface, return a representation of the entity'''
    return jsonify(myWorld.get(entity))


@app.route("/clear", methods=['POST', 'GET'])
def clear():
    '''Clear the world out!'''
    myWorld.clear()
    return jsonify(myWorld.world())


if __name__ == "__main__":
    app.run()
