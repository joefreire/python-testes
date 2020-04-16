#Crawler dos anais do semead
#Author: Guilherme Freire

import requests
import json
from time import sleep
from bs4 import BeautifulSoup
from string import ascii_lowercase
import mysql.connector

ano = 2014
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="root",
  database="semead")
for c in ascii_lowercase:
    inicio = 'http://sistema.semead.com.br/17semead/resultado/an_indiceautor.asp?letra='+c
    resposta = requests.get(inicio, headers={"User-Agent": "Mozilla/5.0"}).content
    soup = BeautifulSoup(resposta, features="html.parser")

    autor = soup.find('td', {"class":"subtitulo"})
    if(autor != None):
        nomeAutor = autor.text.strip()
        proximo = autor.find_next('td', width="9%")
        while (proximo != None):
            artigo = proximo.find_next('a', {"class":"stlink11"})
            if(artigo != None):
                link = artigo.get('href')
                cod = link.split('=')[1]
                nomeArtigo = artigo.text.strip()
                print(nomeAutor, cod, nomeArtigo)
                mycursor = mydb.cursor()
                sql = "INSERT INTO autores(cod, ano, nome) VALUES (%s, %s, %s)"
                val = (cod, ano, nomeAutor)
                mycursor.execute(sql, val)
                mydb.commit()
                mycursor = mydb.cursor()
                sql = "INSERT INTO artigos(cod, ano, titulo) VALUES (%s, %s, %s)"
                val = (cod, ano, nomeArtigo)
                mycursor.execute(sql, val)
                mydb.commit()
                autor = autor.find_next('td', {"class":"subtitulo"})
            if(autor != None ): 
                proximo = autor.find_next('td', width="9%")
                nomeAutor = autor.text.strip()
            else:
                proximo = None
        else:
            print("Acabou")


mycursor = mydb.cursor(dictionary=True)
sql = "SELECT * FROM artigos WHERE ano = %s"
adr = (ano, )
mycursor.execute(sql, adr)
myresult = mycursor.fetchall()

for result in myresult:
    print(result['cod'])
    inicio = 'http://sistema.semead.com.br/19semead/resultado/an_resumo.asp?cod_trabalho='+str(result['cod'])
    resposta = requests.get(inicio, headers={"User-Agent": "Mozilla/5.0"}).content
    soup = BeautifulSoup(resposta, features="html.parser")
    tema = soup.find('td', {"class":"txt12"})

    if "Tema: " in tema:
        print(tema)
    else:
        tema = tema.find_next('td', {"class":"txt12"}).text.strip()
        tema = tema.replace('Tema: ','')
        sql = "UPDATE artigos SET tema =  %s WHERE cod = %s AND ano = %s"
        val = (tema, result['cod'], ano)
        mycursor.execute(sql, val)
        mydb.commit()
        print(tema)