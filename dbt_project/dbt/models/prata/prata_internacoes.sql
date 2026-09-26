-- Grao = internacao. Rollup das avaliacoes de prata_avaliacoes.

with avaliacoes as (

    select * from {{ ref('prata_avaliacoes') }}

),

primeira as (

    select id_internacao, estado_atual as estado_inicial
    from avaliacoes
    qualify row_number() over (
        partition by id_internacao order by data_avaliacao asc
    ) = 1

),

ultima as (

    select id_internacao, estado_atual as estado_final
    from avaliacoes
    qualify row_number() over (
        partition by id_internacao order by data_avaliacao desc
    ) = 1

),

agregado as (

    select
        id_internacao,
        any_value(id_paciente)                              as id_paciente,
        any_value(hospital)                                 as hospital,
        min(data_avaliacao)                                 as data_inicio,
        max(data_avaliacao)                                 as data_fim,
        count(*)                                            as total_avaliacoes,
        avg(pontuacao_seguranca)                            as pontuacao_media,
        max(case when direcao_transicao = 'Escalonar' then 1 else 0 end) = 1
                                                              as teve_escalonamento,
        max(case when direcao_transicao = 'Desescalonar' then 1 else 0 end) = 1
                                                              as teve_desescalonamento
    from avaliacoes
    group by id_internacao

)

select

    a.id_internacao,
    a.id_paciente,
    a.hospital,
    a.data_inicio,
    a.data_fim,
    a.total_avaliacoes,
    a.pontuacao_media,
    a.teve_escalonamento,
    a.teve_desescalonamento,
    p.estado_inicial,
    u.estado_final

from agregado a
left join primeira p on p.id_internacao = a.id_internacao
left join ultima u on u.id_internacao = a.id_internacao
