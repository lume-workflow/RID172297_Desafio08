# Pipeline de Dados com Python e Apache Airflow

Pipeline de dados automatizado construído com Apache Airflow e Docker, que processa dados brutos através de três camadas progressivas de qualidade: Bronze, Prata e Ouro (Medallion Architecture).

---

## 🛠️ Tecnologias Utilizadas

| Tecnologia | Versão | Função |
|---|---|---|
| Python | 3.8 | Processamento e transformação dos dados |
| Apache Airflow | 2.8.1 | Orquestração do pipeline |
| Docker + Docker Compose | 29.x | Ambiente isolado e reproduzível |
| Pandas | latest | Manipulação e análise dos dados |
| PostgreSQL | 13 | Banco de dados interno do Airflow |
| Redis | latest | Fila de mensagens entre os serviços |

---

https://github.com/lume-workflow/RID172297_Desafio08/blob/main/dags/airflow_details.png

## 🏗️ Arquitetura Medallion

O pipeline segue a Medallion Architecture, dividindo o processamento em três camadas com níveis crescentes de qualidade e refinamento dos dados.

### 🥉 Camada Bronze — Dados Brutos
Responsável por ingerir e armazenar os dados originais sem nenhuma modificação. Funciona como um repositório fiel ao arquivo de origem, garantindo que os dados brutos estejam sempre disponíveis para reprocessamento.

- **Entrada:** `raw_data.csv`
- **Saída:** `bronze_data.csv`
- **Transformações:** Nenhuma — cópia fiel dos dados originais

### 🥈 Camada Prata — Dados Limpos
Responsável pela limpeza e padronização dos dados vindos da camada Bronze. Remove inconsistências e enriquece os dados com informações derivadas.

- **Entrada:** `bronze_data.csv`
- **Saída:** `silver_data.csv`
- **Transformações aplicadas:**
  - Remoção de registros com `name`, `email` ou `date_of_birth` nulos
  - Remoção de emails inválidos (sem o caractere `@`)
  - Cálculo da idade de cada usuário com base na data de nascimento

### 🥇 Camada Ouro — Dados Analíticos
Responsável por agregar os dados limpos em um formato pronto para análise e tomada de decisão estratégica.

- **Entrada:** `silver_data.csv`
- **Saída:** `gold_data.csv`
- **Transformações aplicadas:**
  - Classificação dos usuários em faixas etárias (0-10, 11-20, 21-30...)
  - Agregação por faixa etária e status de assinatura (`active` / `inactive`)
  - Geração do total de usuários por grupo

https://github.com/lume-workflow/RID172297_Desafio08/blob/main/dags/airflow_graph.png

---

## ▶️ Como Rodar o Projeto

### Pré-requisitos

- Windows 10/11 com WSL 2 instalado
- Docker Desktop instalado e em execução
- Git instalado

### 1. Clone o repositório

```bash
git clone https://github.com/lume-workflow/RID172297_Desafio08.git
cd RID172297_Desafio08
```

### 2. Crie as pastas necessárias

```bash
mkdir -p data/bronze data/prata data/ouro logs plugins config
```

### 3. Adicione o arquivo de dados brutos

Coloque o arquivo `raw_data.csv` dentro da pasta `data/bronze/`.

### 4. Configure as variáveis de ambiente

```bash
echo -e "AIRFLOW_UID=$(id -u)\nAIRFLOW_GID=0" > .env
```

### 5. Inicialize o Airflow

```bash
docker compose up airflow-init
```

Aguarde até aparecer:
```
User "airflow" created with role "Admin"
```

### 6. Suba os serviços

```bash
docker compose up -d
```

Aguarde todos os contêineres ficarem com status `healthy`:

```bash
docker compose ps
```

### 7. Acesse a interface do Airflow

Abra o navegador em: **http://localhost:8080**

- **Usuário:** `airflow`
- **Senha:** `airflow`

### 8. Execute o pipeline

1. Localize o DAG **`pipeline_medallion`** na lista
2. Ative o DAG clicando no botão de pausa
3. Clique em **▶ Trigger DAG** para executar
4. Acompanhe a execução na aba **Graph**

Após a execução bem-sucedida, os arquivos processados estarão disponíveis em:

```
data/
├── bronze/   → bronze_data.csv
├── prata/    → silver_data.csv
└── ouro/     → gold_data.csv
```

---

## 📁 Estrutura do Projeto

```
RID172297_Desafio08/
├── dags/
│   └── pipeline_dag.py       # DAG principal do Airflow
├── data/
│   ├── bronze/               # Dados brutos
│   ├── prata/                # Dados limpos
│   └── ouro/                 # Dados agregados
├── logs/                     # Logs de execução do Airflow
├── plugins/                  # Extensões do Airflow
├── config/                   # Configurações do Airflow
├── docker-compose.yaml       # Configuração dos serviços Docker
├── .env                      # Variáveis de ambiente
├── .gitignore
├── LICENSE
└── README.md
```

---

## 👤 Autor

**Lume** — [github.com/lume-workflow](https://github.com/lume-workflow)
