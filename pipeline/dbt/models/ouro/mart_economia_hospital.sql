-- Agregado de economia estimada por hospital. Grao = hospital.

select

    hospital,
    count(*)                                                                as total_avaliacoes,
    sum(case when economia_estimada_brl > 0 then 1 else 0 end)              as total_desescalonamentos_efetivados,
    round(sum(economia_estimada_brl), 2)                                    as economia_total_estimada_brl,
    round(avg(case when economia_estimada_brl > 0 then economia_estimada_brl end), 2)
                                                                              as economia_media_por_desescalonamento_brl

from {{ ref('mart_economia_estimada') }}
group by hospital
