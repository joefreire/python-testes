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
            dados_autores[autor] = {
            "universidade": (local[0] if len(local) >= 1 else ''),
            "departamento": (local[1] if len(local) >= 2 else '')
            }
     
    cod = soup.find('a', {"class":"btn btn-success form-control"})
    if(cod != None):
        cod = cod .get('href')
        artigo['cod'] = ''.join([n for n in cod if n.isdigit()])
    else:
        artigo['cod'] = novo.split('=')[1]
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
        if(x.find("h3", text="Tema")):
           artigo["tema"] = x.find("div", "panel-body").text.strip()
                  
    
    artigo["autores"] = dados_autores
    print(artigo)
    with open('data.json', 'a', encoding='utf-8') as f:
        json.dump(artigo, f, ensure_ascii=False, indent=4)
        f.write(",")
    link = soup.find('a', {"class":"btn btn-primary"})
    seta = link.find('span').get("class")
    if 'glyphicon-menu-right' not in seta :
        link = link.findNext('a')
    return link


inicio = 'http://login.semead.com.br/21semead/anais/resumo.php'
resposta = requests.get(inicio, headers={"User-Agent": "Mozilla/5.0"}).content
soup = BeautifulSoup(resposta, features="html.parser")

link = buscaArtigo(soup)

while (link != None):  
  proximo = link.get('href')
  novo = 'http://login.semead.com.br/21semead/anais/resumo.php'+proximo
  print(novo)
  novaResposta = requests.get(novo, headers={"User-Agent": "Mozilla/5.0"}).content
  novoSoup = BeautifulSoup(novaResposta, features="html.parser")
  link = buscaArtigo(novoSoup)
else:
  print("Acabou")


