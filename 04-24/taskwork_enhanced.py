import zmq
import time
import pickle
import sys
from constPipe import *

context = zmq.Context()
me = str(sys.argv[1]) if len(sys.argv) > 1 else "W1"

r = context.socket(zmq.PULL)
p1 = "tcp://" + SRC1 + ":" + PORT1
p2 = "tcp://" + SRC2 + ":" + PORT2
r.connect(p1)
r.connect(p2)

sender = context.socket(zmq.PUSH)
p3 = "tcp://" + SINK + ":" + PORT3
sender.connect(p3)

print(f"[Worker {me}] Conectado a {p1} e {p2}")
print(f"[Worker {me}] Enviando resultados para {p3}")
print("Aguardando tarefas...\n")

tarefas_processadas = 0
carga_total = 0

while True:
    tarefa = pickle.loads(r.recv())
    inicio = time.time()

    tipo = tarefa["tipo"]
    dados = tarefa["dados"]
    carga = tarefa["carga"]

    if tipo == "ordenar":
        resultado = sorted(dados)
    elif tipo == "buscar":
        alvo = dados[0] if dados else 0
        resultado = alvo in dados[1:]
    elif tipo == "calcular":
        resultado = sum(dados)
    else:
        resultado = len(dados)

    time.sleep(carga * 0.01)
    duracao = round(time.time() - inicio, 3)

    tarefas_processadas += 1
    carga_total += carga

    relatorio = {
        "worker": me,
        "tarefa_id": tarefa["id"],
        "origem": tarefa["origem"],
        "tipo": tipo,
        "carga": carga,
        "duracao_s": duracao,
        "resultado": resultado
    }

    sender.send(pickle.dumps(relatorio))
    print(f"  [{me}] Tarefa {tarefa['id']} de src{tarefa['origem']}: "
          f"tipo={tipo}, carga={carga}, tempo={duracao}s "
          f"(total: {tarefas_processadas} tarefas, carga acumulada: {carga_total})")
