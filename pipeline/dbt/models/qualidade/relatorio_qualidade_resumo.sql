-- Camada de Qualidade (3/4): relatorio resumido. Uma linha por execucao
-- do pipeline (materializado como table, sobrescrito a cada dbt run) com
-- os totais gerais de qualidade.

select

    current_timestamp()                                         as gerado_em,
    count(*)                                                     as total_processados,
    sum(case when registro_valido then 1 else 0 end)             as total_validos,
    sum(case when not registro_valido then 1 else 0 end)         as total_rejeitados,
    round(
        100.0 * sum(case when registro_valido then 1 else 0 end) / nullif(count(*), 0),
        2
    )                                                             as pct_qualidade

from {{ ref('formularios_validados') }}
