import zmq
import sys
import json
from constPS import *

context = zmq.Context()
s = context.socket(zmq.SUB)
p = "tcp://" + HOST + ":" + PORT
s.connect(p)

topicos_validos = ["TEMP", "UMID", "ALERTA", "STATUS"]

if len(sys.argv) > 1:
    topicos = [t.upper() for t in sys.argv[1:] if t.upper() in topicos_validos]
else:
    topicos = ["TEMP"]

if not topicos:
    print(f"Topicos validos: {topicos_validos}")
    sys.exit(1)

for topico in topicos:
    s.setsockopt_string(zmq.SUBSCRIBE, topico)

print(f"[Subscriber] Conectado a {p}")
print(f"Inscrito nos topicos: {topicos}")
print("Aguardando mensagens...\n")

contagem = {}
for t in topicos:
    contagem[t] = 0

while True:
    msg = bytes.decode(s.recv())
    partes = msg.split(" ", 1)
    topico = partes[0]
    dados = json.loads(partes[1])

    contagem[topico] = contagem.get(topico, 0) + 1

    if topico == "TEMP":
        print(f"  [TEMP] {dados['cidade']}: {dados['valor']}{dados['unidade']}")
    elif topico == "UMID":
        print(f"  [UMID] {dados['cidade']}: {dados['valor']}{dados['unidade']}")
    elif topico == "ALERTA":
        print(f"  *** [ALERTA] {dados['cidade']}: {dados['tipo']} ({dados['temp']}C) ***")
    elif topico == "STATUS":
        print(f"  [STATUS] Ciclos: {dados['mensagens_enviadas']} | {dados['timestamp']}")

    total = sum(contagem.values())
    if total % 10 == 0:
        print(f"  --- Recebidas: {contagem} ---")
