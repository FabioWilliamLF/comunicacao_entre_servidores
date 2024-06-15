from socket import *
import socketserver
import ping_automaticoAtt
from prettytable import PrettyTable
import shutil

contador = 0

def menu():
    connection.send(f"""
Escolha uma opção:
1 - Para efetuar um ping e retornar o resultado
2 - Para ver a lista de pings feito anteriormente nesta execução
3 - Para sair e armazenar a lista de pings em um CLS
Escolha: """.encode('utf-8'))

myHost = 'localhost'

myPort = 50007

list_ping = []
datas = []
horas = []
ips = []
urls = []
avable = []

ativo = "IP ativo e informações salvas"
inativo = "IP fora do ar, mas as informações foram salvas"

socketServer = socket(AF_INET,SOCK_STREAM)

socketServer.bind((myHost,myPort))

socketServer.listen()
print("Servidor na escuta...")

connection, adress = socketServer.accept()
print("COnexão aceita")

print("-----------------COmunicação-------------------")
try:
    while True:

        if contador == 3:
            connection.close()
            break
        
        senha = connection.recv(1024)
        if senha.decode('utf-8') != "123":
            contador += 1
            connection.send(f"Senha incorreta! tentativas: {contador}/3".encode('utf-8'))
            continue
        elif senha.decode('utf-8') == "123":
            
            break

    connection.send("Senha Correta!".encode('utf-8'))
    while True:
        

        msgRcv = connection.recv(1024)


        
        if msgRcv.decode('utf-8') not in ["1", "2", "3"]:
            menu()
            
        if msgRcv.decode('utf-8') == "3":
            connection.send("Selecione a pasta...:".encode('utf-8'))
            pasta = connection.recv(1024)
            print(pasta.decode('utf-8'))
            ping_automaticoAtt.armazena_ping(urls, ips, avable, datas, horas)
            shutil.move('ping_automatico.csv', pasta.decode('utf-8'))
            break

        if msgRcv.decode('utf-8') == "1":
            connection.send('Digite a URL que deseja efetuar o ping: '.encode('utf-8'))

            new = connection.recv(1024)

            ip = ping_automaticoAtt.efetuar_ping(new.decode('utf-8')).encode('utf-8')
            ips.append(ip)
            list_ping.append(new.decode('utf-8').encode('utf-8'))
            datas.append(ping_automaticoAtt.gera_dia_atual())
            horas.append(ping_automaticoAtt.gera_hora_atual())
            urls.append(new.decode('utf-8'))
            avables = ping_automaticoAtt.verify_available(new.decode('utf-8')).encode('utf-8')
            avable.append(avables)
            print("---------------------------------------------------------------------------------------------")
            print("---------------------------------------------------------------------------------------------")

            if avables == b"Fora do ar":
                connection.send(f"""
    IP fora do ar, mas as informações foram salvas. 
    URL = {new.decode('utf-8').encode('utf-8')}
    IP = {ip}
    Numero de pacotes enviados = {ping_automaticoAtt.nmrpak}
    Digite OK para continuar""".encode('utf-8'))
            else:
                connection.send(f"""
    IP ativo e informações salvas. Digite OK para continuar
    URL = {new.decode('utf-8').encode('utf-8')}
    IP = {ip}
    Numero de pacotes enviados = {ping_automaticoAtt.nmrpak}
    Digite OK para continuar""".encode('utf-8'))
                
        if msgRcv.decode('utf-8') == "2":
            tabela = PrettyTable()
            tabela.add_column("URL", urls)
            tabela.add_column("IP", ips)
            tabela.add_column("Status", avable)
            tabela.add_column("Data", datas)
            tabela.add_column("Hora", horas)

            connection.send(f"""
    {tabela}
    Digite OK para continuar.
                            """.encode('utf-8'))


    connection.close()
except:
    print('Acesso negado!')