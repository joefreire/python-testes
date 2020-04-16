#Crawler dos anais do semead
#Author: Guilherme Freire

import requests
import json
from time import sleep
from bs4 import BeautifulSoup
from string import ascii_lowercase
import mysql.connector

ano = 2015
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="root",
  database="semead")
mycursor = mydb.cursor(dictionary=True)
sql = "SELECT * FROM artigos WHERE ano = %s"
adr = (ano, )
mycursor.execute(sql, adr)
myresult = mycursor.fetchall()

result = myresult[0]

tema = result['tema']
mycursor = mydb.cursor(dictionary=True)
sql = "SELECT * FROM areas WHERE tema LIKE %s"
adr = ("%" + tema + "%", )
mycursor.execute(sql, adr)
area = mycursor.fetchall()
print(area[0]['nome'])