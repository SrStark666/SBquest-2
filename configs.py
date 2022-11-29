from time import sleep
from colorama import Fore
import subprocess
import requests
import os.path
import bs4
import sys
import re


class Request:
    #PathSelector = {"https://www.pockettactics.com/{game}/codes": "#site_wrap div.entry-content ul:first-of-type li"}
    def __init__(self, game: str) -> None:
        self.url = [f"https://www.pockettactics.com/{game}/codes", f"https://progameguides.com/roblox/roblox-{game}-codes", f"https://tryhardguides.com/{game}-codes"]
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, como Gecko) Chrome/45.0.2454.85 Safari/537.36"}
        self.game = str(game).replace(" ", "-") #Filtra os dados da string em um formato aceitável para a requisição
        self.valid_codes = {} #Armazena os códigos do jogo
        self.found = [] #Urls verificadas pela função verify_request
        self.done = len(self.found) #Quantidade de sites válidos


    def verify_request(self) -> None: #Verifica os sites que possuem os códigos do jogo
        for url in self.url:
            get = requests.get(url, headers=self.headers)
            if get.status_code == 200:
                self.found.append(url)
            elif get.status_code != 200:
                url = url.split("roblox-")
                convert = url[0]+url[1]
                treatment = requests.get(convert, headers=self.headers)
                if treatment.status_code == 200:
                    self.found.append(convert)
                else:
                    print(f"\033[01;31mJogo não encontrado no site: \033[0m{convert}\n\033[01;31mVerifique a entrada de dados!!\033[0m")    

        self.done = len(self.found)
        if len(self.found) == 0:
            print(f"Verifique sua digitação!!")


    def soup(self) -> list[bs4.BeautifulSoup]: #Retorna os objetos soup dentro de uma lista
        soups = []
        if self.done != 0:
            for url in self.found:
                get = requests.get(url, headers=self.headers)
                tx = get.text
                soup_obj = bs4.BeautifulSoup(tx, "html.parser")
                soups.append(soup_obj)

        return soups


    def find_tag(self, soup) -> list[bs4.element.Tag]: #Procura as tags dentro do objeto soup
        codes = []
        for soups in soup:
            for ul in soups.find_all("ul"):
                for li in ul.find_all("li"):
                    for _ in li.find_all("strong"):
                        codes.append(li.text)

        self.len_tags = len(codes)
        return codes


    def filter(self, sopa) -> None: #Filtrando os códigos e adicionando no atributo self.valid_codes
        for valids in self.find_tag(sopa):
            valids = valids.replace(u'\xa0', u' ').replace("!", "").replace("(New)", "").replace("(new)", "").replace("(NEW)", "")
            conv = [s.strip() for s in re.split("[-–—:]", valids)] #["Código", "Descrição"]

            if not self.valid_codes: #Len 0
                if len(conv) == 1:
                    self.valid_codes[conv[0]] = "Indefinido"
                elif len(conv) == 2 and conv[1] != "":
                    self.valid_codes[conv[0]] = conv[1]

            elif conv[0] in self.valid_codes:
                pass

            elif len(conv) > 1:
                self.valid_codes[conv[0]] = conv[1]

        if "Network Sites" in self.valid_codes:
            del self.valid_codes["Network Sites"]


    def loading(self) -> None: #Animação de loading
        icons = ["|", "/", "-", "\\"]
        limit = 100
        while limit > 0:
            for i in icons:
                sys.stdout.write(f"\r\033[01;33mLoading {i}\033[0m")
                limit -= 1
                sleep(.1)

        sys.stdout.flush()
        print(f"\n\033[01;32mConcluído\033[0m")

    
    def archive(self, name, valid_codes) -> None:
        if not re.search(name, ".txt"):
            name += ".txt"

        if not os.path.exists(f"Codes/"):
            subprocess.run("mkdir Codes", shell=True, universal_newlines=True)

        with open(f"Codes/{name}", "w+") as arq:
            for codes in valid_codes:
                treatment_code = re.split("[-–—:]", str(codes))[0]
                treatment_info = re.split("[-–—:]", str(codes))[1]
                if len(treatment_code) < 2:
                    indefinied = f"{treatment_code} >>> Indefinido"
                    arq.write(f"{indefinied}\n")
                else:
                    wr = f"{treatment_code} >>> {treatment_info}"
                    arq.write(f"{wr}\n")

            print(f"{Fore.GREEN}Arquivo criado com sucesso!!{Fore.RESET}")