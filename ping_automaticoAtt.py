import subprocess
import csv
from datetime import datetime

nmrpak = "3"

#executa o ping
def ping(cmd):
    execute = subprocess.Popen(cmd, stdout=subprocess.PIPE, text=True)
    out, err = execute.communicate()
    return out

#verifica disponibilidade
def verify_available(domain):
    reply = subprocess.run(['ping', '-c', '3', '-n', domain],
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE,
                           encoding='utf-8')
    if reply.returncode == 0:
        return "Ativo"
    else:
        return "Fora do ar"


#gera o dia atual
def gera_dia_atual():
    dia_atual = datetime.now()
    data = dia_atual.strftime("%d/%m/%Y")
    return str(data)

#gera a hora atual
def gera_hora_atual():
    hora_atual = datetime.now()
    hora = hora_atual.strftime("%H:%M:%S")
    return str(hora)

#cria o arquivo de armazenamento
def criando_o_arquivo_armazenamento():  
    with open('ping_automatico.csv', 'w', newline='') as csvfile:
            fieldnames = ['URL', 'IP', 'STATUS', 'DATA', 'HORA']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()

#adiciona informações no arquivo 
def adicionando_no_arquivo(URL, IP, STATUS):
    with open('ping_automatico.csv', 'w', newline='1') as csvfile:
        fieldnames = ['URL', 'IP', 'STATUS', 'DATA', 'HORA']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writerow({'URL': str(URL), 'IP': str(IP), 'STATUS': str(STATUS), 'DATA': gera_dia_atual(), 'HORA': gera_hora_atual()})


#cria o arquivo

def efetuar_ping(dominio):

            reply = subprocess.run(["ping", "-c", nmrpak, "-n", dominio], 
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            encoding='utf-8')
            
            print(reply.stdout)
                
            procurar_ip = reply.stdout
            output_lines = procurar_ip.split("\n")
            status = verify_available(dominio)
            #caso não localize o ip, o ip será N/A
            ip_address = "N/A"

            #faz um for de linha por linha para procurar o IP no retorno do ping no CMD
            for line in output_lines:
                if "PING" in line:
                    #inicio de onde vai começar a captura do arquivo
                    inicio = 0
                    #fim e -1 para não pegar o ultimo ")"
                    fim = -1
                    #começa o for
                    for caracter in line:
                        inicio += 1
                        if caracter == "(":
                            break
                    for caracter in line:
                        fim += 1
                        if caracter == ")":
                            break
                    #mostra onde está o IP
                    ip_address = line[inicio:fim]
                    break
            
            if status == "Ativo":
                return ip_address
            else:
                return ip_address
            
def armazena_ping(url, ip, status, data, hora):
    with open('ping_automatico.csv', 'w', newline='') as csvfile:
            fieldnames = ['URL', 'IP', 'STATUS', 'DATA', 'HORA']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            criando_o_arquivo_armazenamento()
            
            for d in range(len(url)):

                writer.writerow({'URL': url[d], 'IP': ip[d], 'STATUS': status[d], 'DATA': data[d], 'HORA': hora[d]})
        