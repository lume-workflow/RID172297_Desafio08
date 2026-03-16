# Pipeline de Dados com Python e Apache Airflow

## O problema

Dados brutos são, na maioria das vezes, inutilizáveis do jeito que chegam. Campos vazios, emails inválidos, datas sem tratamento — tudo isso impede que um analista extraia qualquer insight confiável.

Além disso, sem automação, um engenheiro precisa executar manualmente cada etapa do processo toda vez que os dados forem atualizados. Isso é lento, sujeito a erro humano e não escala.

Esse projeto resolve os dois problemas: automatiza o processamento de dados de ponta a ponta e entrega um dataset limpo e agregado, pronto para análise.

---

## O que o pipeline responde

> *Quantos usuários existem por faixa etária e qual é a proporção entre ativos e inativos?*

Com essa informação, uma empresa pode identificar, por exemplo, que existe uma concentração de usuários inativos entre 21 e 30 anos — uma oportunidade clara para campanhas de reativação direcionadas.

---

## O pipeline em execução

[![Grafo do pipeline](https://raw.githubusercontent.com/lume-workflow/data-pipeline-airflow-docker/main/dags/airflow_graph.png)](https://raw.githubusercontent.com/lume-workflow/data-pipeline-airflow-docker/main/dags/airflow_graph.png)


[![Detalhes da execução](https://raw.githubusercontent.com/lume-workflow/data-pipeline-airflow-docker/main/dags/airflow_details.png)](https://raw.githubusercontent.com/lume-workflow/data-pipeline-airflow-docker/main/dags/airflow_details.png)


## Como funciona

O pipeline segue a **Medallion Architecture**, processando os dados em três camadas progressivas:

**🥉 Bronze — dados como vieram**
O arquivo bruto é carregado sem nenhuma modificação. Essa camada existe para garantir rastreabilidade: se algo der errado nas etapas seguintes, sempre é possível voltar à origem.

**🥈 Prata — dados limpos**
Aqui os dados são tratados: registros com campos essenciais vazios são removidos, emails inválidos são descartados e a idade de cada usuário é calculada a partir da data de nascimento.

**🥇 Ouro — dados prontos para decisão**
Os dados limpos são agregados em faixas etárias (0-10, 11-20, 21-30...) e separados por status de assinatura. O resultado é uma tabela direta, pronta para um analista ou gestor usar.

---

## Tecnologias

- **Python + Pandas** — processamento e transformação dos dados
- **Apache Airflow** — orquestração e agendamento do pipeline
- **Docker** — ambiente isolado e reproduzível (necessário pois o Airflow não roda nativamente no Windows)

---

## O que aprendi construindo isso

**Sobre dados:** manter as camadas separadas é o que permite diagnosticar onde um problema começou quando algo dá errado em produção. Sem isso, você perde a capacidade de rastrear a origem de qualquer inconsistência.

**Sobre orquestração:** Python puro executa quando você manda. O Airflow executa quando o negócio precisa: com agendamento, monitoramento visual e reprocessamento a partir do ponto de falha, sem precisar rodar tudo do zero.

**Sobre Docker:** o problema que ele resolve não é técnico, é humano. "Na minha máquina funciona" é uma frase que destrói tempo e confiança em times de dados. O Docker elimina essa variável, garantindo que não tenha um choque inesperado entre versões incompatíveis.

**O que eu melhoraria numa versão 2:** validações mais robustas na camada Prata, alertas automáticos por email em caso de falha, e PySpark para suportar volumes maiores de dados sem sobrecarregar a memória.

---

## Como rodar

**Pré-requisitos:** WSL 2, Docker Desktop e Git instalados.

```bash
# Clone o repositório
git clone https://github.com/lume-workflow/data-pipeline-airflow-docker.GIT
cd data-pipeline-airflow-docker

# Crie as pastas necessárias
mkdir -p data/bronze data/prata data/ouro logs plugins config

# Adicione o arquivo raw_data.csv dentro de data/bronze/

# Configure as variáveis de ambiente
echo -e "AIRFLOW_UID=$(id -u)\nAIRFLOW_GID=0" > .env

# Inicialize o Airflow
docker compose up airflow-init

# Suba os serviços
docker compose up -d
```

Acesse **http://localhost:8080** com usuário `airflow` e senha `airflow`, ative o DAG `pipeline_medallion` e clique em **Trigger DAG**.

---

## Autor

**Lume** — [github.com/lume-workflow](https://github.com/lume-workflow)
