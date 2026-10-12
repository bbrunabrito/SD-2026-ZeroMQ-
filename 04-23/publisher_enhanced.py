import zmq
import time
import random
import json
from constPS import *

context = zmq.Context()
s = context.socket(zmq.PUB)
p = "tcp://" + BIND + ":" + PORT
s.bind(p)

print(f"[Publisher] Rodando em {p}")
print("Publicando topicos: TEMP, UMID, ALERTA, STATUS\n")

cidades = ["Sao Paulo", "Rio de Janeiro", "Belo Horizonte", "Curitiba", "Salvador"]
cont = 0

while True:
    time.sleep(2)
    cont += 1

    cidade = random.choice(cidades)
    temp = round(random.uniform(15.0, 40.0), 1)
    umid = round(random.uniform(30.0, 95.0), 1)

    msg_temp = json.dumps({"cidade": cidade, "valor": temp, "unidade": "C"})
    s.send(str.encode(f"TEMP {msg_temp}"))
    print(f"  Publicado: TEMP {cidade} = {temp}C")

    msg_umid = json.dumps({"cidade": cidade, "valor": umid, "unidade": "%"})
    s.send(str.encode(f"UMID {msg_umid}"))

    if temp > 35.0:
        alerta = json.dumps({
            "cidade": cidade,
            "tipo": "CALOR EXTREMO",
            "temp": temp
        })
        s.send(str.encode(f"ALERTA {alerta}"))
        print(f"  *** ALERTA: {cidade} com {temp}C!")

    if cont % 5 == 0:
        status = json.dumps({
            "mensagens_enviadas": cont,
            "timestamp": time.asctime()
        })
        s.send(str.encode(f"STATUS {status}"))
        print(f"  STATUS: {cont} ciclos publicados")
