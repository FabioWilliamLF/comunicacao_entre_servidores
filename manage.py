import subprocess

local = ""
pasta_selkt = ""
pasta_att = []

reply = subprocess.run(["pwd", "cd"], 
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            encoding='utf-8')

pastas = reply.stdout.rstrip().split("/")



def sele_pasta():
    while True:
        for x in range(len(pastas)):
            if pastas[x] == '':
                continue
            else:
                print(f" digite {x} para selecionar a pasta: {pastas[x]}")

        try:    
            escolhido = int(input("Digite o número da sua opção escolida: "))
            for x in range(len(pastas)):
                
                if x == escolhido + 1:
                    local = "/".join(pasta_att)
                    break
                else:
                    pasta_att.append(pastas[x])
            return local
        except:
                input("Valor escolhido inválido, Enter para tentar novamente.")
                continue