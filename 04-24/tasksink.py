import zmq
import pickle
import time
from constPipe import *

context = zmq.Context()

r = context.socket(zmq.PULL)
p = "tcp://" + BIND + ":" + PORT3
r.bind(p)

print(f"[Sink] Coletando resultados em {p}")
print("Aguardando resultados dos workers...\n")

resultados = []
stats_workers = {}
inicio = time.time()

try:
    while True:
        relatorio = pickle.loads(r.recv())
        resultados.append(relatorio)

        w = relatorio["worker"]
        if w not in stats_workers:
            stats_workers[w] = {"tarefas": 0, "carga": 0, "tempo": 0.0}
        stats_workers[w]["tarefas"] += 1
        stats_workers[w]["carga"] += relatorio["carga"]
        stats_workers[w]["tempo"] += relatorio["duracao_s"]

        print(f"  Resultado #{len(resultados)}: Worker {w} | "
              f"Tarefa {relatorio['tarefa_id']} (src{relatorio['origem']}) | "
              f"tipo={relatorio['tipo']} | {relatorio['duracao_s']}s")

        if len(resultados) % 10 == 0:
            print(f"\n  === Relatorio parcial ({len(resultados)} resultados) ===")
            for worker, stats in stats_workers.items():
                print(f"    {worker}: {stats['tarefas']} tarefas, "
                      f"carga total={stats['carga']}, "
                      f"tempo total={round(stats['tempo'], 2)}s")
            print()

except KeyboardInterrupt:
    elapsed = round(time.time() - inicio, 2)
    print(f"\n\n=== RELATORIO FINAL ===")
    print(f"Total de resultados: {len(resultados)}")
    print(f"Tempo total: {elapsed}s")
    print(f"\nDesempenho por worker:")
    for worker, stats in sorted(stats_workers.items()):
        media = round(stats["tempo"] / stats["tarefas"], 3) if stats["tarefas"] > 0 else 0
        print(f"  {worker}: {stats['tarefas']} tarefas | "
              f"carga={stats['carga']} | "
              f"tempo={round(stats['tempo'], 2)}s | "
              f"media={media}s/tarefa")
