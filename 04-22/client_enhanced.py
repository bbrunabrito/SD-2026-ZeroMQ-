import zmq
import json
from constCS import *

context = zmq.Context()

p1 = "tcp://" + HOST + ":" + PORT1
s = context.socket(zmq.REQ)
s.connect(p1)

print("=== Cliente Calculadora ===")
print("Operacoes: soma, sub, mult, div, pot, raiz, fatorial, historico")
print("Digite 'sair' para encerrar o servidor.\n")

while True:
    entrada = input("Operacao (ex: soma 10 5): ").strip()

    if not entrada:
        continue

    if entrada.lower() == "sair":
        s.send(b"STOP")
        resp = s.recv()
        print(bytes.decode(resp))
        break

    partes = entrada.split()
    op = partes[0]

    req = {"op": op}
    if len(partes) >= 2:
        try:
            req["a"] = float(partes[1])
        except ValueError:
            print("Valor invalido para 'a'.")
            continue
    if len(partes) >= 3:
        try:
            req["b"] = float(partes[2])
        except ValueError:
            print("Valor invalido para 'b'.")
            continue

    s.send(str.encode(json.dumps(req)))
    resp = s.recv()
    resultado = json.loads(bytes.decode(resp))
    print(f"  Resultado: {resultado['resultado']}\n")
