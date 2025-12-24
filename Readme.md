# 🚀 Pipeline_ETL – Users Enrichment Pipeline

Este repositório implementa um **pipeline ETL (Extract, Transform, Load)** em Python, responsável por **consumir uma API de usuários**, **enriquecer os dados** e **persistir as atualizações** de volta na API.

⚠️ **Importante**: este projeto **NÃO é a API**. Ele é o **consumidor/orquestrador ETL** que opera sobre a API `users-api-etl`.

---

## 📌 Objetivo do Projeto

Demonstrar um **ETL real e funcional**, integrando:

* Consumo de API REST
* Processamento e enriquecimento de dados
* Escrita de volta via endpoints REST (`PUT /users/:id`)

O pipeline foi pensado para ser **simples, reproduzível e extensível**, seguindo boas práticas de engenharia de dados.

---

## 🔁 Visão Geral do ETL

```
┌──────────┐      ┌────────────┐      ┌──────────┐
│ Extract  │ ───▶ │ Transform  │ ───▶ │  Load    │
└──────────┘      └────────────┘      └──────────┘
   GET /users        Enriquecimento      PUT /users/:id
```

---

## 🧩 Etapas do Pipeline

### 1️⃣ Extract – Coleta dos dados

O pipeline inicia consumindo a API de usuários:

```python
GET https://users-api-etl.up.railway.app/users
```

O retorno é carregado em memória como lista de dicionários Python.

---

### 2️⃣ Transform – Enriquecimento

Nesta etapa, os dados são transformados. Exemplo:

* Geração de mensagens personalizadas
* Inserção de conteúdo informativo (ex: investimentos)
* Preparação de estrutura compatível com a API

```python
user["news"].append({
    "icon": "https://digitalinnovationone.github.io/santander-dev-week-2023-api/icons/credit.svg",
    "description": "Invista no seu futuro hoje"
})
```

Esta etapa pode ser facilmente estendida para:

* uso de LLMs
* regras de negócio
* scoring ou segmentação

---

### 3️⃣ Load – Persistência dos dados

Os dados enriquecidos são enviados de volta para a API:

```python
PUT https://users-api-etl.up.railway.app/users/{id}
```

Exemplo de implementação:

```python
def update_user(user):
    payload = {"news": user["news"]}
    response = requests.put(
        f"{API_URL}/{user['id']}",
        json=payload
    )
    return response.status_code == 200
```

---

## 📂 Estrutura do Projeto (ETL)

```
dataprocess_etl/
│
├── etl.ipynb        # Pipeline ETL (Extract → Transform → Load)
├── requirements.txt
├── README.md
```

---

## ⚙️ Tecnologias Utilizadas

* **Python 3.9+**
* **requests**
* API REST (Users API)

---

## ▶️ Execução do Pipeline

1. Configure o ambiente:

```bash
pip install -r requirements.txt
```

2. Execute o pipeline:

```bash
jupyter notebook etl.ipynb
```

---

## ✅ Resultado Esperado

```
User Ana Pereira updated? True!
User Pyterson updated? True!
User Pip updated? True!
```

---

## 🔮 Possíveis Evoluções

* Agendamento (cron / Airflow)
* Versionamento do pipeline
* Logs estruturados
* Retry e controle de falhas
* Integração com LLMs

---

## 🧠 Conclusão

Este repositório representa um **pipeline ETL completo**, desacoplado da API, seguindo um modelo realista de integração entre sistemas.

> A API é apenas a fonte/destino. O valor está no pipeline.

---

✍️ Projeto: **Pipeline_ETL**


John Peter Oyardo Manrique
jpomanrique@gmail.com
