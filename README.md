# Project TCC — Avaliação de Transição de Nível de Cuidado

Projeto de TCC (Pós-Graduação em Engenharia de Dados) que reproduz, de forma
independente e sem nenhum dado real de empresa, a arquitetura de um produto
de gestão hospitalar: um formulário clínico vira dado bruto, passa por um
pipeline de dados em camadas, e chega como indicador num dashboard.

## O produto, em uma frase

Um profissional (o "médico gerenciador") avalia, a cada visita, se um
paciente internado pode mudar de nível de cuidado com segurança — sair da
UTI, ir para Home Care, ou precisar escalonar para a UTI. O sistema registra
essa decisão, calcula de forma independente se os critérios clínicos
concordam com ela, e mostra isso num dashboard de gestão.

## As duas partes do projeto

```
project_tcc/
├── apps/formulario_transicao/   # 1. Formulário (Databricks App / Streamlit)
├── src/project_tcc/services/    # Código Python compartilhado do app
└── pipeline/                    # 2. Pipeline de dados (dbt + Databricks)
```

### 1. Formulário (`apps/formulario_transicao/`)

App Streamlit rodando como Databricks App. O profissional preenche:
estado atual do paciente, direção da transição pretendida (Manter /
Desescalonar / Escalonar), os critérios clínicos objetivos, e uma
justificativa. Ao enviar, `src/project_tcc/services/storage.py` grava um
arquivo JSON no Volume `pipeline_tcc.ingestao.formularios_json` — é aqui que
o dado "nasce".

### 2. Pipeline de dados (`pipeline/`)

Tudo que transforma esse JSON bruto em indicador. Ver
[`pipeline/README.md`](pipeline/README.md) para detalhes técnicos (como
rodar localmente, como fazer deploy). Resumo da estrutura:

```
pipeline/
├── src/ingest_bronze.py     # Ingestão: JSON -> tabela Delta (camada Bronze)
├── dbt/models/
│   ├── staging/             # Tipagem e organização do dado bruto
│   ├── intermediate/        # Onde o indicador é calculado
│   ├── prata/                # Avaliações e internações consolidadas
│   └── ouro/                 # Tabelas finais que o dashboard consome
├── resources/                # Definição do Job e do Dashboard no Databricks
├── dashboards/                # Dashboard de indicadores (AI/BI)
└── databricks.yml            # Empacota tudo isso como um deploy só
```

## Como o dado flui, passo a passo

1. Profissional preenche o formulário → vira um arquivo JSON no Volume de
   ingestão.
2. A chegada do arquivo dispara automaticamente um Job no Databricks (não
   precisa de ninguém rodando nada manualmente).
3. O Job faz duas coisas, em sequência:
   - **Ingestão**: lê o JSON e grava como tabela Delta (`bronze.formularios`).
   - **dbt**: transforma esse dado bruto em camadas, terminando nas 3 tabelas
     da camada Ouro.
4. **O indicador central**: o pipeline calcula, a partir só dos critérios
   clínicos preenchidos, qual seria a direção de transição recomendada — e
   compara com o que o profissional realmente decidiu. Também verifica se a
   transição sugerida de fato aconteceu na avaliação seguinte.
5. O **dashboard** lê as tabelas da camada Ouro e mostra: quantas avaliações
   no total, % de concordância entre indicador e decisão real, pontuação de
   segurança média, e comparativos por hospital e por profissional.

## Stack

| Peça | Ferramenta |
|---|---|
| Formulário | Streamlit, rodando como Databricks App |
| Armazenamento bruto | Volume (Unity Catalog) |
| Transformação | dbt |
| Orquestração | Databricks Jobs (file arrival trigger) |
| Dashboard | AI/BI Dashboard (Databricks Lakeview) |
| Deploy | Databricks Asset Bundles |
| CI/CD | GitHub Actions — valida em todo PR pra `main`, deploya quando o PR é mergeado |

## Time

Jeander, Joabe e Lianderson.
