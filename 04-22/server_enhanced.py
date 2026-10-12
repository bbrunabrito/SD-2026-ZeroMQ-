import zmq
import json
import math
import datetime
from constCS import *

context = zmq.Context()

p1 = "tcp://" + BIND + ":" + PORT1
s = context.socket(zmq.REP)
s.bind(p1)

print(f"[Servidor Calculadora] Rodando em {p1}")
print("Operacoes suportadas: soma, sub, mult, div, pot, raiz, fatorial")
print("Aguardando requisicoes...\n")

log = []

def processar(req):
    op = req.get("op", "").lower()
    a = req.get("a", 0)
    b = req.get("b", 0)

    if op == "soma":
        return a + b
    elif op == "sub":
        return a - b
    elif op == "mult":
        return a * b
    elif op == "div":
        if b == 0:
            return "ERRO: divisao por zero"
        return a / b
    elif op == "pot":
        return a ** b
    elif op == "raiz":
        if a < 0:
            return "ERRO: raiz de numero negativo"
        return math.sqrt(a)
    elif op == "fatorial":
        if a < 0 or int(a) != a:
            return "ERRO: fatorial requer inteiro positivo"
        return math.factorial(int(a))
    elif op == "historico":
        return log[-10:]
    else:
        return f"ERRO: operacao '{op}' desconhecida"

while True:
    msg = s.recv()
    decoded = bytes.decode(msg)

    if "STOP" in decoded:
        s.send(str.encode("Servidor encerrado."))
        print("Servidor encerrado pelo cliente.")
        break

    try:
        req = json.loads(decoded)
    except json.JSONDecodeError:
        s.send(str.encode(json.dumps({"erro": "JSON invalido"})))
        continue

    resultado = processar(req)

    entrada = {
        "horario": str(datetime.datetime.now()),
        "requisicao": req,
        "resultado": resultado
    }
    log.append(entrada)

    print(f"  [{entrada['horario']}] {req} -> {resultado}")

    resposta = json.dumps({"resultado": resultado})
    s.send(str.encode(resposta))
