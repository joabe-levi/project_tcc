-- Window functions por internacao: olha a proxima avaliacao (LEAD) pra saber
-- se a transicao sugerida numa avaliacao de fato aconteceu, e quanto tempo
-- levou ate a proxima avaliacao.

with stg as (

    -- so segue registro que passou na camada de qualidade (ver models/qualidade)
    select * from {{ ref('formularios_validados') }}
    where registro_valido

),

sequencia as (

    select
        id_formulario,
        id_internacao,
        estado_atual,
        data_avaliacao,

        lead(estado_atual) over (
            partition by id_internacao order by data_avaliacao
        )                                                   as proximo_estado_real,

        lead(data_avaliacao) over (
            partition by id_internacao order by data_avaliacao
        )                                                   as data_proxima_avaliacao_real

    from stg

)

select

    id_formulario,
    id_internacao,
    proximo_estado_real,
    data_proxima_avaliacao_real,

    (proximo_estado_real is not null and proximo_estado_real != estado_atual)
                                                              as transicao_efetivada_real,

    case
        when data_proxima_avaliacao_real is not null
        then (unix_timestamp(data_proxima_avaliacao_real) - unix_timestamp(data_avaliacao)) / 3600.0
    end                                                       as horas_ate_proxima_avaliacao

from sequencia
