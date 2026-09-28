-- Camada de Qualidade (2/4): quarentena. So os registros que falharam em
-- pelo menos uma regra de `formularios_validados` ficam aqui, junto com o
-- motivo. NAO seguem para intermediate/prata/ouro -- isolados pra
-- inspecao/correcao manual, sem travar o resto do pipeline.

select

    id_formulario,
    id_internacao,
    id_paciente,
    hospital,
    data_avaliacao,
    estado_atual,
    direcao_transicao,
    pontuacao_seguranca,
    motivos_rejeicao,
    current_timestamp() as quarentena_em

from {{ ref('formularios_validados') }}
where not registro_valido
