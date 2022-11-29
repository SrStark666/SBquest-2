from colorama import Fore
import configs
import re


try:
    while True:
        game = str(input(f"{Fore.YELLOW}Digite o nome do jogo: {Fore.RESET}").replace(" ", "-")).lower()

        obj = configs.Request(game) #Cria o objeto classe
        request = obj.verify_request() #Requisição e verificação dos sites
        soup = obj.soup() #Transforma os sites válidos em objetos soup dentro de uma lista
        find = obj.find_tag(soup) #Busca as tags que armazenam os códigos
        codes = obj.filter(soup) #Filtra os códigos e adiciona na lista self.valid_codes

        for code in obj.valid_codes: #Retira caracteres indesejados dos códigos
            if obj.valid_codes[code] == "Indefinido":
                obj.valid_codes[code] = "\033[01;31mIndefinido\033[0m"

            print(f"{Fore.CYAN}{code}{Fore.RESET} >>> {Fore.MAGENTA}{obj.valid_codes[code]}{Fore.RESET}")

        for sites in obj.found:
            print(f"{Fore.MAGENTA}Site verificado: {sites}")

        print(f"{Fore.GREEN}Códigos encontrados: {len(obj.valid_codes)}{Fore.RESET}")
        choice = str(input(f"{Fore.YELLOW}Deseja salvar em um arquivo? S/n {Fore.RESET}")).lower()
        if choice == "s" or choice == "sim":
            archive = str(input(f"{Fore.YELLOW}Nome do arquivo: {Fore.RESET}"))
            obj.archive(archive, obj.valid_codes)
            break
        elif choice == "n" or choice == "não" or choice == "nao":
            break
        else:
            print(f"{Fore.RED}Erro na entrada de dados{Fore.RESET}")
            break
except KeyboardInterrupt:
    print(f"{Fore.RESET}Programa encerrado{Fore.RESET}")

