-- Agregados operacionais por profissional. Grao = profissional. Serve como
-- proxy de quao conservador/agressivo cada profissional tende a ser nas
-- decisoes de transicao.

select

    id_profissional,
    nome_profissional,
    count(*)                                                            as total_avaliacoes,
    round(avg(case when flag_concordancia then 1.0 else 0.0 end), 4)    as pct_concordancia,
    round(avg(pontuacao_seguranca), 2)                                  as pontuacao_media,
    sum(case when direcao_transicao = 'Manter' then 1 else 0 end)       as total_manter,
    sum(case when direcao_transicao = 'Desescalonar' then 1 else 0 end) as total_desescalonar,
    sum(case when direcao_transicao = 'Escalonar' then 1 else 0 end)    as total_escalonar

from {{ ref('prata_avaliacoes') }}
group by id_profissional, nome_profissional
