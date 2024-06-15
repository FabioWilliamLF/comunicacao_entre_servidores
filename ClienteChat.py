from socket import *
import socketserver
import manage

login = False
contador = 0
myHost = 'localhost'

myPort = 50007

socketClient = socket(AF_INET, SOCK_STREAM)


print("Cliente solicitando conexão...")

socketClient.connect((myHost,myPort))

login = input("Digite o login: ")
while True:

    if login == True:
        break

    if contador == 3:
        socketClient.close()
        print("Pedido de conexão negado!")
        break

    senha = input("Digite a senha: ")
    socketClient.send(senha.encode('utf-8'))
    resposta = socketClient.recv(1024).decode('utf-8')
    print(resposta)
    if resposta == "Senha Correta!":
        login = True
        break
        
    elif resposta != "Senha Correta!":
        contador += 1
        print(resposta)
        continue

    



while True:
    
    msg = input("Cliente diz: ")
    

    if msg == "3":
        socketClient.send(msg.encode('utf-8'))
        mensagem = socketClient.recv(1024)
        print(mensagem.decode('utf-8'))
        socketClient.send(manage.sele_pasta().encode('utf-8'))
        break
    else:
        socketClient.send(msg.encode('utf-8'))
        msgServidor = socketClient.recv(1024)
        print(f"Servidor diz: {msgServidor.decode('utf-8')} ")
        continue

socketClient.close()