# Sistemas Distribuidos - ZeroMQ

Exemplos de comunicacao distribuida usando a biblioteca **ZeroMQ** (pyzmq) em Python, demonstrando tres padroes fundamentais de messaging: **Request-Reply**, **Publish-Subscribe** e **Pipeline**.

## Instalacao

### Requisitos

- Python 3.8+
- pyzmq

### Configuracao do ambiente virtual (recomendado)

```bash
python3 -m venv venv
source venv/bin/activate        # Linux/Mac
# ou
venv\Scripts\activate           # Windows
pip install pyzmq
```

### Instalacao direta

```bash
pip3 install pyzmq
```

---

## Visao Geral dos Padroes ZeroMQ

| Padrao | Diretorio | Sockets | Descricao |
|--------|-----------|---------|-----------|
| Request-Reply | `04-22/` | REQ/REP | Cliente envia requisicao, servidor responde |
| Publish-Subscribe | `04-23/` | PUB/SUB | Publisher transmite, subscribers filtram por topico |
| Pipeline | `04-24/` | PUSH/PULL | Distribuicao de tarefas entre workers |

---

## 04-22 — Request-Reply (REQ/REP)

### Descricao

Padrao cliente-servidor sincrono. O cliente envia uma mensagem e bloqueia ate receber a resposta do servidor.

### Arquivos originais

- `server.py` — Servidor que recebe mensagens e devolve com `*` anexado
- `client.py` — Cliente que envia "Hello world" e recebe resposta
- `client1.py` / `client2.py` — Clientes conectando em portas diferentes
- `constCS.py` — Constantes de conexao (HOST e PORTs)

### Versao aprimorada (novas funcionalidades)

- `server_enhanced.py` — **Servidor calculadora** com suporte a operacoes matematicas (soma, sub, mult, div, pot, raiz, fatorial), comunicacao via JSON, log de requisicoes com timestamps, e consulta de historico
- `client_enhanced.py` — **Cliente interativo** que permite digitar operacoes pelo terminal, exibindo resultados formatados

### Como executar

**Terminal 1 — Servidor:**
```bash
python server_enhanced.py
```

**Terminal 2 — Cliente:**
```bash
python client_enhanced.py
```

**Exemplos de uso no cliente:**
```
soma 10 5       -> 15.0
mult 3 7        -> 21.0
raiz 144        -> 12.0
fatorial 6      -> 720
div 10 0        -> ERRO: divisao por zero
historico       -> ultimas 10 operacoes
sair            -> encerra servidor
```

### Funcionalidades adicionadas

1. Protocolo de comunicacao estruturado com JSON
2. Sete operacoes matematicas (soma, sub, mult, div, pot, raiz, fatorial)
3. Tratamento de erros (divisao por zero, raiz negativa, JSON invalido)
4. Log com timestamp de todas as requisicoes no servidor
5. Comando `historico` para consultar ultimas operacoes

---

## 04-23 — Publish-Subscribe (PUB/SUB)

### Descricao

Padrao de comunicacao assincrona um-para-muitos. O publisher transmite mensagens em topicos e os subscribers recebem apenas as mensagens dos topicos que assinaram.

### Arquivos originais

- `publisher.py` — Publica horario atual a cada 5 segundos no topico "TIME"
- `subscriber.py` — Assina o topico "TIME" e recebe 5 mensagens
- `constPS.py` — Constantes de conexao

### Versao aprimorada (novas funcionalidades)

- `publisher_enhanced.py` — **Estacao meteorologica simulada** que publica dados de temperatura (TEMP), umidade (UMID), alertas automaticos (ALERTA) quando temperatura > 35C, e status periodico (STATUS) para 5 cidades brasileiras
- `subscriber_enhanced.py` — **Subscriber com filtro por topicos via linha de comando**, contagem de mensagens recebidas, e exibicao formatada por tipo

### Como executar

**Terminal 1 — Publisher:**
```bash
python publisher_enhanced.py
```

**Terminal 2 — Subscriber de temperatura:**
```bash
python subscriber_enhanced.py TEMP
```

**Terminal 3 — Subscriber de alertas e status:**
```bash
python subscriber_enhanced.py ALERTA STATUS
```

**Terminal 4 — Subscriber de todos os topicos:**
```bash
python subscriber_enhanced.py TEMP UMID ALERTA STATUS
```

### Funcionalidades adicionadas

1. Quatro topicos distintos (TEMP, UMID, ALERTA, STATUS)
2. Dados estruturados em JSON com informacoes de cidade, valor e unidade
3. Alertas automaticos gerados quando temperatura excede 35C
4. Selecao de topicos via argumentos de linha de comando
5. Contagem e relatorio de mensagens recebidas por topico
6. Simulacao de dados para 5 cidades brasileiras

---

## 04-24 — Pipeline (PUSH/PULL)

### Descricao

Padrao de distribuicao de trabalho. Fontes (PUSH) geram tarefas e workers (PULL) as consomem, com balanceamento automatico de carga pelo ZeroMQ.

### Arquivos originais

- `tasksrc.py` — Fonte de tarefas que gera 100 cargas de trabalho aleatorias
- `taskwork.py` — Worker que recebe e processa tarefas de duas fontes
- `constPipe.py` — Constantes de conexao

### Versao aprimorada (novas funcionalidades)

- `tasksrc_enhanced.py` — **Fonte de tarefas tipadas** que gera tarefas com tipo (calcular, ordenar, buscar, processar), dados associados e metadados
- `taskwork_enhanced.py` — **Worker inteligente** que processa cada tipo de tarefa de forma diferente (soma, ordenacao, busca, contagem) e envia resultados para um coletor
- `tasksink.py` — **Coletor de resultados (Sink)** que agrega resultados, gera estatisticas por worker, e produz relatorio final com metricas de desempenho

### Como executar

**Terminal 1 — Sink (iniciar primeiro):**
```bash
python tasksink.py
```

**Terminal 2 — Worker 1:**
```bash
python taskwork_enhanced.py W1
```

**Terminal 3 — Worker 2:**
```bash
python taskwork_enhanced.py W2
```

**Terminal 4 — Fonte de tarefas 1:**
```bash
python tasksrc_enhanced.py 1
```

**Terminal 5 — Fonte de tarefas 2 (opcional):**
```bash
python tasksrc_enhanced.py 2
```

O Sink exibe relatorios parciais a cada 10 resultados. Para ver o relatorio final, pressione `Ctrl+C` no Sink.

### Funcionalidades adicionadas

1. Tarefas tipadas com quatro categorias (calcular, ordenar, buscar, processar)
2. Processamento especifico por tipo de tarefa nos workers
3. Componente **Sink** (coletor) para agregar resultados — completa o padrao Pipeline
4. Medicao de tempo de processamento por tarefa
5. Relatorios parciais automaticos e relatorio final com estatisticas
6. Metadados em cada tarefa (id, tipo, carga, dados)
7. Metricas de desempenho por worker (tarefas, carga, tempo medio)

---

## Configuracao para Maquinas Diferentes (AWS)

Para executar em maquinas diferentes, edite o arquivo `const*.py` de cada exemplo, substituindo `localhost` pelo IP privado da maquina que roda o servidor/publisher/source.

### Exemplo para AWS EC2

1. Crie 2+ instancias EC2 (Amazon Linux 2 ou Ubuntu)
2. Configure o **Security Group** para liberar as portas TCP usadas (4567, 4568, 4569)
3. Instale o Python e pyzmq em todas as maquinas:
   ```bash
   sudo yum install python3 -y       # Amazon Linux
   # ou
   sudo apt install python3 python3-pip -y  # Ubuntu
   pip3 install pyzmq
   ```
4. Edite os arquivos de constantes com o IP privado do servidor:
   ```python
   # constCS.py na maquina do servidor (04-22)
   HOST  = "172.31.X.X"   # IP privado da instancia do servidor
   PORT1 = "4567"
   PORT2 = "4568"
   ```
5. Copie os arquivos para as instancias (ex: via `scp`):
   ```bash
   scp -i chave.pem *.py ec2-user@<IP-publico>:~/
   ```
6. Execute o servidor em uma maquina e o cliente em outra

### Regras do Security Group

| Tipo | Protocolo | Porta | Origem |
|------|-----------|-------|--------|
| Custom TCP | TCP | 4567 | Security Group ID |
| Custom TCP | TCP | 4568 | Security Group ID |
| Custom TCP | TCP | 4569 | Security Group ID |

---

## Estrutura do Projeto

```
SD-2026-ZeroMQ-/
├── README.md
├── 04-22/                      # Request-Reply (REQ/REP)
│   ├── constCS.py              # Constantes de conexao
│   ├── server.py               # Servidor original
│   ├── client.py               # Cliente original
│   ├── client1.py              # Cliente porta 1
│   ├── client2.py              # Cliente porta 2
│   ├── server_enhanced.py      # Servidor calculadora (aprimorado)
│   └── client_enhanced.py      # Cliente interativo (aprimorado)
├── 04-23/                      # Publish-Subscribe (PUB/SUB)
│   ├── constPS.py              # Constantes de conexao
│   ├── publisher.py            # Publisher original
│   ├── subscriber.py           # Subscriber original
│   ├── publisher_enhanced.py   # Estacao meteorologica (aprimorado)
│   └── subscriber_enhanced.py  # Subscriber multi-topico (aprimorado)
└── 04-24/                      # Pipeline (PUSH/PULL)
    ├── constPipe.py            # Constantes de conexao
    ├── tasksrc.py              # Fonte de tarefas original
    ├── taskwork.py             # Worker original
    ├── tasksrc_enhanced.py     # Fonte de tarefas tipadas (aprimorado)
    ├── taskwork_enhanced.py    # Worker inteligente (aprimorado)
    └── tasksink.py             # Coletor de resultados (novo)
```

---

## Autora

Bruna de Brito Alves
