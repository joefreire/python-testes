#Crawler dos anais do semead
#Author: Guilherme Freire

import requests
import json
from time import sleep
from bs4 import BeautifulSoup


def buscaArtigo(soup):
    artigo = {}
    dados_autores = {}
    autores = soup.find("tbody").find_all("td")
    for y in autores:
        local = y.find("small").text.strip()
        local = local.split(" - ")
        for small in y.find_all("small"):
            small.replaceWith("")
            autor = y.text.strip()
            autor = autor.split(" - ")
            autor_posicao = autor[0]
            autor = autor[1]
            dados_autores[autor_posicao] = {"nome":autor, "universidade":local[0], "departamento":local[1]}
     

    mydivs = soup.find_all("div", ["panel", "panel-default"])
    for x in mydivs:
        if(x.find("h3", text="Título do Artigo")):
            artigo["titulo"] = x.find("div", "panel-body").text.strip()
        if(x.find("h3", text="Palavras Chave")):
            keywords = x.find("div", "panel-body").text.strip()
            keywords = keywords.split("\n")
            artigo["keywords"] = [i.strip() for i in keywords]
        if(x.find("h3", text="Área")):
           artigo["area"] = x.find("div", "panel-body").text.strip()
                  
    artigo["autores"] = dados_autores 

    print(artigo["titulo"])
    with open('data.json', 'a', encoding='utf-8') as f:
        json.dump(artigo, f, ensure_ascii=False, indent=4)
        json.dump(',', f, ensure_ascii=False, indent=4)



inicio = 'http://login.semead.com.br/21semead/anais/resumo.php'
resposta = requests.get(inicio, headers={"User-Agent": "Mozilla/5.0"}).content
soup = BeautifulSoup(resposta, features="html.parser")
buscaArtigo(soup)
#
# link = soup.find('a', {"class":"btn btn-primary"})
# while (link != None):
#   buscaArtigo(soup)
#   proximo = link.get('href')
#   inicio = 'http://login.semead.com.br/21semead/anais/resumo.php'+proximo
#   print(inicio)
#   resposta = requests.get(inicio, headers={"User-Agent": "Mozilla/5.0"}).content
#   soup = BeautifulSoup(resposta, features="html.parser")
# else:
#   print("Acabou")


