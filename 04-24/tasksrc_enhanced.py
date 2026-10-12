import zmq
import time
import pickle
import sys
import random
from constPipe import *

context = zmq.Context()
me = str(sys.argv[1]) if len(sys.argv) > 1 else "1"

s = context.socket(zmq.PUSH)
prt = PORT1 if me == "1" else PORT2
p = "tcp://" + BIND + ":" + prt
s.bind(p)

tipos_tarefa = ["calcular", "ordenar", "buscar", "processar"]
n_tarefas = 20

print(f"[TaskSrc {me}] Rodando em {p}")
print(f"Gerando {n_tarefas} tarefas...\n")

total_carga = 0

for i in range(n_tarefas):
    time.sleep(0.5)
    carga = random.randint(1, 100)
    tipo = random.choice(tipos_tarefa)
    dados = random.sample(range(1, 1000), min(carga, 50))

    tarefa = {
        "origem": me,
        "id": i + 1,
        "tipo": tipo,
        "carga": carga,
        "dados": dados
    }

    s.send(pickle.dumps(tarefa))
    total_carga += carga
    print(f"  Tarefa {i+1}: tipo={tipo}, carga={carga}")

print(f"\n[TaskSrc {me}] Finalizado. Carga total: {total_carga}")
