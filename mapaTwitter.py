#!/usr/bin/python
# -*- coding: utf-8 -*

__author__ ='KevValle'
from flask import Flask, render_template
from flask import request
from flask.ext.googlemaps import GoogleMaps
from flask.ext.googlemaps import Map

import twitter
import io
import json
import sys

#Elegimos un tema en concreto, se le pasa como argumento al ejecutar el programa
#if len(sys.argv) > 1:
#    tema = sys.argv[1]
#else:
#    tema = "SD"

#Función para conectar a twitter
def oauth_login():
    CONSUMER_KEY = 'uKAS8Tx4UItk5NI2u8jQPH8VV'
    CONSUMER_SECRET = 'rro3oGH5cz8Z2OgiNKFIY0JSoQX9CBDhI8AAEYZUzAjCVE4AP1'
    OAUTH_TOKEN = '359375683-hGVHDpenpwlpUKwtbMbyvShuzMsQEHxvrwNGWlqL'
    OAUTH_TOKEN_SECRET = '4piR2vrGimMI2OMuzuXKNHXBNYNH9cejoWQIwx9yPh6EI'
    
    auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET)

    twitter_api = twitter.Twitter(auth=auth)
    return twitter_api

#Funciones para grabar y leer de archivos JSON
def save_json(filename, data):
    with io.open('{0}.json'.format(filename),'w', encoding='utf-8') as f:
        f.write(unicode(json.dumps(data, ensure_ascii=False)))

def load_json(filename):
    with io.open('{0].json'.format(filename),encoding='utf-8') as f:
        return f.read()

#Conectamos a twitter
sesion = oauth_login()

def busqueda(tema):
    #Buscamos los tweets que tengan el tema dado por el usuario
    tweets = sesion.search.tweets(q=tema,count=1000,geocode='40.45,-3.75,1000km')
    
    #Guardamos en JSON los tweets y luego los cargamos
    save_json('tweets', tweets)
    tweetsJSON = json.loads(open('tweets.json').read())

    #Se analizan los tweets y solo se guardan los que necesitamos
    sitioTweets = []

    for result in tweetsJSON["statuses"]:
        if result["geo"]:
            latitud = result["geo"]["coordinates"][0]
            longitud = result["geo"]["coordinates"][1]
            coord=[latitud,longitud]
            sitioTweets.append(coord)

    return sitioTweets

#Finalmente se crea el mapa
app = Flask(__name__)
GoogleMaps(app)

@app.route("/buscar", methods =['POST'])
def mapview():
    tema = request.form['text']
    sitioTweets = busqueda(tema)
    mymap = Map(
        identifier="view-side",
        lat=40.45,
        lng=-3,
        markers=sitioTweets,
        style="height:800px;width:800px;margin:0",
        zoom=6
    )
    return render_template('mapa.html', mymap=mymap)

@app.route("/")
def index():
	return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True) 
