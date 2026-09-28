# Dicionário de dados

Catalog `pipeline_tcc` (Unity Catalog). Todas as tabelas da camada `bronze` em
diante são Delta, geradas pelo pipeline dbt (`pipeline/dbt/`).

## `ingestao.formularios_json` (Volume — bruto)

Arquivos JSON individuais, um por avaliação preenchida no formulário. Ver
estrutura completa em `formulario-avaliacao-transicao-spec.pdf` (raiz do
projeto). Grão = 1 arquivo por avaliação.

## `bronze.formularios`

1:1 com o JSON bruto, sem tratamento. Grão = avaliação.

| Campo | Tipo | Descrição |
|---|---|---|
| id_formulario | string | UUID do formulário (chave natural) |
| id_internacao | string | UUID da internação |
| id_paciente | string | UUID do paciente |
| id_profissional / nome_profissional | string | Profissional que avaliou |
| data_avaliacao | string (ISO 8601) | Timestamp da avaliação |
| hospital | string | Nome do hospital |
| estado_atual / estado_recomendado | string | Nível de cuidado atual e recomendado pelo app |
| direcao_transicao | string | Manter / Desescalonar / Escalonar (decisão do profissional) |
| criterios_avaliados | struct | 8 critérios de segurança + 2 de alerta (booleanos) |
| pontuacao_seguranca | int | 0–10, calculada pelo app no momento do preenchimento |
| justificativa | string | Texto livre |
| data_prevista_transicao | string | Data (se direção ≠ Manter) |

## `qualidade.formularios_validados`

Aplica 9 regras de validação sobre `bronze.formularios` (via `stg_formularios`). Grão = avaliação.

| Campo | Tipo | Descrição |
|---|---|---|
| (todos os campos de `bronze.formularios`, tipados) | — | — |
| chk_* (9 colunas) | boolean | Uma por regra de validação (ver `docs/arquitetura.md`) |
| registro_valido | boolean | `true` somente se todas as 9 regras passaram |
| motivos_rejeicao | string | Lista das regras que falharam, separadas por vírgula |

## `qualidade.quarentena_formularios`

Só os registros com `registro_valido = false`. Grão = avaliação rejeitada.

| Campo | Tipo | Descrição |
|---|---|---|
| id_formulario, id_internacao, id_paciente, hospital, data_avaliacao, estado_atual, direcao_transicao, pontuacao_seguranca | — | Campos originais, para inspeção |
| motivos_rejeicao | string | Por que foi rejeitado |
| quarentena_em | timestamp | Quando entrou em quarentena (momento do `dbt run`) |

## `qualidade.relatorio_qualidade_resumo`

1 linha por execução do pipeline (sobrescrita a cada `dbt run`).

| Campo | Tipo | Descrição |
|---|---|---|
| gerado_em | timestamp | Momento da execução |
| total_processados | int | Total de avaliações no staging |
| total_validos / total_rejeitados | int | Quantos passaram / falharam na validação |
| pct_qualidade | float | `total_validos / total_processados * 100` |

## `qualidade.relatorio_qualidade_por_regra`

Grão = regra de validação (9 linhas).

| Campo | Tipo | Descrição |
|---|---|---|
| regra | string | Identificador da regra |
| descricao | string | Descrição legível |
| total_falhas | int | Quantos registros falharam nessa regra especificamente |

## `prata.prata_avaliacoes`

Grão = avaliação (só registros válidos). Junta o indicador calculado com a sequência real da internação.

| Campo | Tipo | Descrição |
|---|---|---|
| id_formulario, id_internacao, id_paciente, id_profissional, nome_profissional | string | Identificadores |
| data_avaliacao, hospital, estado_atual, estado_recomendado | — | Contexto da avaliação |
| direcao_transicao | string | Decisão real do profissional |
| direcao_recomendada_calculada | string | Direção que os critérios recomendariam (indicador) |
| flag_concordancia | boolean | `direcao_transicao = direcao_recomendada_calculada` |
| total_criterios_favoraveis / total_criterios_alerta | int | Contagem dos 8 + 2 critérios |
| pontuacao_seguranca | int | — |
| proximo_estado_real, data_proxima_avaliacao_real | — | Próxima avaliação da mesma internação (LEAD) |
| transicao_efetivada_real | boolean | Se o estado realmente mudou na avaliação seguinte |
| horas_ate_proxima_avaliacao | float | — |

## `prata.prata_internacoes`

Grão = internação (rollup de `prata_avaliacoes`).

| Campo | Tipo | Descrição |
|---|---|---|
| id_internacao, id_paciente, hospital | — | Identificadores |
| data_inicio, data_fim, total_avaliacoes | — | Janela temporal da internação |
| pontuacao_media | float | Média das avaliações |
| teve_escalonamento / teve_desescalonamento | boolean | Se algum evento do tipo ocorreu |
| estado_inicial / estado_final | string | Primeiro e último estado observado |

## `ouro.mart_transicoes`

Indicador central. Grão = avaliação. Colunas: `id_formulario`, `id_internacao`, `hospital`, `nome_profissional`, `data_avaliacao`, `estado_atual`, `direcao_transicao`, `direcao_recomendada_calculada`, `flag_concordancia`, `transicao_efetivada_real`, `pontuacao_seguranca`, `total_criterios_favoraveis`, `total_criterios_alerta`, `horas_ate_proxima_avaliacao`.

**Perguntas de negócio que responde:**
1. *Os profissionais concordam com o que os critérios clínicos recomendariam?* → `avg(flag_concordancia)`.
2. *Quando uma transição é recomendada, ela de fato acontece?* → `avg(transicao_efetivada_real)`.

## `ouro.mart_operacional_hospital` / `ouro.mart_operacional_profissional`

Grão = hospital / profissional. Agregados: `total_avaliacoes`, `pct_concordancia`, `pontuacao_media`, `horas_medias_ate_proxima_avaliacao`, `total_manter`/`total_desescalonar`/`total_escalonar`.

**Pergunta de negócio:** *Existe diferença de comportamento (conservador vs. agressivo) entre hospitais ou profissionais?*

## `ouro.seed_custo_diario_leito`

Seed de referência (não é dado observado). Grão = estado. Colunas: `estado`, `custo_diario_brl` (estimativa, ver nota em `pipeline/dbt/seeds/_seeds__properties.yml`).

## `ouro.mart_economia_estimada` / `ouro.mart_economia_hospital`

Grão = avaliação / hospital. Colunas principais: `economia_estimada_brl` (só > 0 quando um desescalonamento recomendado foi efetivado), `economia_total_estimada_brl`, `total_desescalonamentos_efetivados`.

**Pergunta de negócio:** *Quanto a ferramenta economiza, em termos de custo de leito, ao ajudar a identificar desescalonamentos seguros?*

## `ouro.mart_adocao_produto`

Grão = mês. Colunas: `mes`, `total_avaliacoes`, `hospitais_ativos`, `profissionais_ativos`, `internacoes_ativas`.

**Pergunta de negócio:** *O uso da ferramenta está crescendo?* (indicador de produto/comercial, não clínico)
