import tweepy
import unidecode
import json
import re
import csv
consumer_key = "bACQ2drpynaMBberGMJ7kRQDU"
consumer_secret = "ZKYRlIaBiA2ieTLQrV0zu2b1YuzEvzMooL1Rjye9Vv5HXiUFAg"
access_token = "810912048943157248-qjellrxYIqOqqJQXN9MRWJ6GSQeIFpD"
access_token_secret = "AB7lcwlV4xP7CFuXMZOr04ed8yvGnwAfSWZoupqRuHFZY"
auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token,access_token_secret)

def generarTweet(consulta, cantidad, dateS, dateU):
    api = tweepy.API(auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)
    places = api.geo_search(query="ECU", granularity="country")
    place = places[0]
    date_since = dateS
    date_until = dateU
    texto, datos = ([] for i in range(2))
    cont=0
    contar=0
    for tweet in tweepy.Cursor(api.search, q="%s en %s -filter:retweets" %(consulta,place.name), lang="es", since=date_since, until=date_until, tweet_mode='extended').items(cantidad):
        dic1 = tweet._json["created_at"]
        dic2 = tweet._json["user"]
        dic3 = tweet._json["full_text"] ##o de esta manera print(tweet.full_text)
        n = unidecode.unidecode(dic2["name"])
        d = unidecode.unidecode(dic3).replace('\n', ' ')#Remplaza todas los caracteres especiales
        dsinlinks = re.sub(r'http\S+', '', d)
        dsinarroba = re.sub(r'@+', '', dsinlinks)
        dsinslash = re.sub('[^A-Za-z0-9]+', ' ',dsinarroba)
        if dsinslash not in texto:
            texto.append(dsinslash)
            datos.append([dic1, n, dsinslash])
            contar=+contar+1
        else:
            cont=+cont+1
    print("Total de tweets: ",cantidad)
    print("Cadenas No Iguales: ",contar)
    print("Cadenas Iguales: ",cont)
    return datos