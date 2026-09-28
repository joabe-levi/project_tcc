-- Camada de Qualidade (1/4): validacao linha a linha de todo formulario
-- vindo do staging. Cada regra vira uma coluna booleana; um registro so
-- segue para o resto do pipeline (intermediate/prata/ouro) se passar em
-- TODAS as regras (registro_valido = true). Quem falha fica visivel aqui
-- e e capturado por `quarentena_formularios` (model seguinte).
--
-- Grao = avaliacao. 1:1 com stg_formularios, sem filtrar nada -- e o
-- proprio filtro que os models seguintes usam.

with stg as (

    select * from {{ ref('stg_formularios') }}

),

checks as (

    select

        *,

        (id_formulario is not null
            and id_formulario rlike '^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$')
                                                                as chk_id_formulario_valido,

        (id_internacao is not null and id_internacao != '')    as chk_id_internacao_preenchido,

        (id_paciente is not null and id_paciente != '')        as chk_id_paciente_preenchido,

        (data_avaliacao is not null)                           as chk_data_avaliacao_valida,

        (hospital is not null and hospital != '')               as chk_hospital_preenchido,

        (estado_atual in ('UTI', 'Semi-UTI', 'Enfermaria', 'Home Care'))
                                                                as chk_estado_atual_valido,

        (direcao_transicao in ('Manter', 'Desescalonar', 'Escalonar'))
                                                                as chk_direcao_transicao_valida,

        (pontuacao_seguranca is not null
            and pontuacao_seguranca between 0 and 10)          as chk_pontuacao_seguranca_valida,

        (crit_estabilidade_hemodinamica is not null
            and crit_sinais_instabilidade_aguda is not null)   as chk_criterios_preenchidos

    from stg

)

select

    *,

    (chk_id_formulario_valido
        and chk_id_internacao_preenchido
        and chk_id_paciente_preenchido
        and chk_data_avaliacao_valida
        and chk_hospital_preenchido
        and chk_estado_atual_valido
        and chk_direcao_transicao_valida
        and chk_pontuacao_seguranca_valida
        and chk_criterios_preenchidos)                          as registro_valido,

    trim(both ', ' from concat(
        case when not chk_id_formulario_valido then 'id_formulario_invalido, ' else '' end,
        case when not chk_id_internacao_preenchido then 'id_internacao_vazio, ' else '' end,
        case when not chk_id_paciente_preenchido then 'id_paciente_vazio, ' else '' end,
        case when not chk_data_avaliacao_valida then 'data_avaliacao_invalida, ' else '' end,
        case when not chk_hospital_preenchido then 'hospital_vazio, ' else '' end,
        case when not chk_estado_atual_valido then 'estado_atual_fora_do_dominio, ' else '' end,
        case when not chk_direcao_transicao_valida then 'direcao_transicao_fora_do_dominio, ' else '' end,
        case when not chk_pontuacao_seguranca_valida then 'pontuacao_seguranca_fora_da_faixa, ' else '' end,
        case when not chk_criterios_preenchidos then 'criterios_nao_preenchidos, ' else '' end
    ))                                                            as motivos_rejeicao

from checks
