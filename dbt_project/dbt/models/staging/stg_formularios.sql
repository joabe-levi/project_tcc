-- Staging: tipagem + flatten dos criterios_avaliados do JSON bruto.
-- 1:1 em grao com a bronze (1 linha por avaliacao/formulario).

with bronze as (

    select * from {{ source('bronze', 'formularios') }}

)

select

    id_formulario,
    id_internacao,
    id_paciente,
    id_profissional,
    nome_profissional,
    cast(data_avaliacao as timestamp)              as data_avaliacao,
    hospital,
    estado_atual,
    estado_recomendado,
    direcao_transicao,
    cast(pontuacao_seguranca as int)               as pontuacao_seguranca,
    justificativa,
    cast(data_prevista_transicao as date)          as data_prevista_transicao,
    observacoes,

    -- criterios de seguranca (8)
    criterios_avaliados.estabilidade_hemodinamica          as crit_estabilidade_hemodinamica,
    criterios_avaliados.sem_suporte_ventilatorio           as crit_sem_suporte_ventilatorio,
    criterios_avaliados.sem_drogas_vasoativas              as crit_sem_drogas_vasoativas,
    criterios_avaliados.nivel_consciencia_preservado       as crit_nivel_consciencia_preservado,
    criterios_avaliados.dor_controlada_via_oral            as crit_dor_controlada_via_oral,
    criterios_avaliados.aceitacao_dieta_oral               as crit_aceitacao_dieta_oral,
    criterios_avaliados.mobilidade_compativel_proximo_nivel as crit_mobilidade_compativel_proximo_nivel,
    criterios_avaliados.suporte_familiar_disponivel        as crit_suporte_familiar_disponivel,

    -- criterios de alerta (2)
    criterios_avaliados.sinais_instabilidade_aguda         as crit_sinais_instabilidade_aguda,
    criterios_avaliados.necessidade_monitorizacao_continua as crit_necessidade_monitorizacao_continua

from bronze
