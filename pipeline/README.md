# pipeline_tcc — Bronze/Prata/Ouro no Databricks

Pipeline de dados do TCC (reprodução independente do fluxo "Médico
Gerenciador", sem dado real de empresa). Um profissional preenche um
formulário de avaliação clínica (ver `formulario-avaliacao-transicao-spec.pdf`
na raiz do projeto); o preenchimento vira JSON bruto, é ingerido em Bronze via
Auto Loader, transformado em camadas via dbt (Prata/Ouro), tudo orquestrado
por um Job do Databricks definido como Databricks Asset Bundle (DAB) e
publicado via GitHub Actions.

## Arquitetura

```
Volume pipeline_tcc.ingestao.formularios_json   (JSON bruto)
        |  Auto Loader (src/ingest_bronze.py)
pipeline_tcc.bronze.formularios                 (Delta, sem tratamento)
        |  dbt staging + intermediate
pipeline_tcc.prata.avaliacoes / .internacoes     (Delta, enriquecido)
        |  dbt marts
pipeline_tcc.ouro.mart_transicoes
pipeline_tcc.ouro.mart_operacional_hospital
pipeline_tcc.ouro.mart_operacional_profissional
```

O indicador central (`mart_transicoes`) compara a decisão real do
profissional (`direcao_transicao`) com uma direção calculada de forma
independente a partir dos critérios de segurança/alerta preenchidos no
formulário (`direcao_recomendada_calculada`), e verifica se a transição
sugerida de fato aconteceu na avaliação seguinte (`transicao_efetivada_real`).

## Estrutura do repositório

```
databricks.yml            # bundle: nome, target(s), host do workspace
resources/jobs.yml         # Job: file-arrival trigger + task ingestao + task dbt
resources/dashboards.yml   # Dashboard AI/BI (Lakeview) sobre as marts Ouro
src/ingest_bronze.py       # Auto Loader: volume JSON -> Delta bronze.formularios
dashboards/pipeline_tcc_indicadores.lvdash.json   # definicao do dashboard
dbt/
  dbt_project.yml
  models/
    staging/               # stg_formularios: tipagem + flatten dos criterios
    intermediate/           # regra do indicador + sequencia (LEAD por internacao)
    prata/                  # avaliacoes (grao=avaliacao) e internacoes (rollup)
    ouro/                   # os 3 marts finais
```

## Dashboard

`resources/dashboards.yml` publica um dashboard AI/BI (Lakeview) direto no
Databricks, consumindo as 3 marts Ouro:

- KPIs: total de avaliações, % de concordância (indicador calculado vs.
  decisão real do profissional), pontuação de segurança média, % de
  transições efetivadas na avaliação seguinte.
- Distribuição das avaliações por direção de transição (Manter/
  Desescalonar/Escalonar).
- % de concordância por hospital e por profissional.
- Tabelas de detalhe por hospital, por profissional e por avaliação.

É deployado junto com o resto do bundle (`databricks bundle deploy`); depois
do deploy, o link fica disponível em `databricks bundle summary -t dev`
(campo `resources.dashboards.pipeline_tcc_indicadores.url`).

## Rodar localmente

Pré-requisitos: Python 3.10+, [Databricks CLI](https://docs.databricks.com/dev-tools/cli/index.html)
autenticado (`databricks configure`), pacote `dbt-databricks`.

```bash
pip install dbt-databricks

# profiles.yml local (NAO commitar; usar variaveis de ambiente ou ~/.dbt/profiles.yml)
# host: dbc-24e63c87-e011.cloud.databricks.com
# http_path: /sql/1.0/warehouses/5937853489eb21c0
# catalog: pipeline_tcc
# token: <seu PAT pessoal>

cd dbt
dbt debug
dbt build
```

## Deploy no Databricks (via bundle)

```bash
databricks bundle validate -t dev
databricks bundle deploy -t dev
databricks bundle run pipeline_tcc_medallion   # dispara uma execucao manual
```

O Job também dispara sozinho por *file arrival trigger* sempre que chegam
arquivos novos no volume de ingestão — não precisa rodar manualmente no dia a
dia.

## CI/CD

`.github/workflows/ci.yml`: toda PR roda `databricks bundle validate`; todo
merge em `main` roda `databricks bundle deploy -t dev`. Requer os secrets do
repositório `DATABRICKS_HOST` e `DATABRICKS_TOKEN`.

## Validar resultados

- `dbt test` (ou `dbt build`, que já roda run+test): 0 falhas esperadas.
- Contagem de linhas esperada (dataset sintético atual): `bronze.formularios`
  e `ouro.mart_transicoes` = 217 linhas; `prata.internacoes` = 60 linhas;
  `mart_operacional_hospital` até 5 linhas; `mart_operacional_profissional`
  até 6 linhas.
