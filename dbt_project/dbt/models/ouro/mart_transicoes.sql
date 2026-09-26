-- Mart central do TCC: indicador de transicao recomendada (calculada pelos
-- criterios) vs. transicao realizada (decisao do profissional). Grao = avaliacao.

select

    id_formulario,
    id_internacao,
    hospital,
    nome_profissional,
    data_avaliacao,
    estado_atual,
    direcao_transicao,
    direcao_recomendada_calculada,
    flag_concordancia,
    transicao_efetivada_real,
    pontuacao_seguranca,
    total_criterios_favoraveis,
    total_criterios_alerta,
    horas_ate_proxima_avaliacao

from {{ ref('prata_avaliacoes') }}
