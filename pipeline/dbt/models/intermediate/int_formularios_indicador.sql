-- Aplica a regra do indicador de forma independente da decisao do
-- profissional: a partir dos criterios/pontuacao, calcula qual seria a
-- direcao recomendada, e compara com o que o profissional de fato registrou.
--
-- Regra (documentada no plano de execucao do TCC):
--   alerta >= 1                -> 'Escalonar'
--   senao pontuacao_seguranca >= 6 -> 'Desescalonar'
--   senao                        -> 'Manter'

with stg as (

    -- so segue registro que passou na camada de qualidade (ver models/qualidade)
    select * from {{ ref('formularios_validados') }}
    where registro_valido

),

calc as (

    select
        *,

        (case when crit_estabilidade_hemodinamica then 1 else 0 end)
        + (case when crit_sem_suporte_ventilatorio then 1 else 0 end)
        + (case when crit_sem_drogas_vasoativas then 1 else 0 end)
        + (case when crit_nivel_consciencia_preservado then 1 else 0 end)
        + (case when crit_dor_controlada_via_oral then 1 else 0 end)
        + (case when crit_aceitacao_dieta_oral then 1 else 0 end)
        + (case when crit_mobilidade_compativel_proximo_nivel then 1 else 0 end)
        + (case when crit_suporte_familiar_disponivel then 1 else 0 end)
                                                            as total_criterios_favoraveis,

        (case when crit_sinais_instabilidade_aguda then 1 else 0 end)
        + (case when crit_necessidade_monitorizacao_continua then 1 else 0 end)
                                                            as total_criterios_alerta

    from stg

)

select

    *,

    case
        when total_criterios_alerta >= 1 then 'Escalonar'
        when pontuacao_seguranca >= 6     then 'Desescalonar'
        else 'Manter'
    end                                                     as direcao_recomendada_calculada,

    case
        when direcao_transicao = (
            case
                when total_criterios_alerta >= 1 then 'Escalonar'
                when pontuacao_seguranca >= 6     then 'Desescalonar'
                else 'Manter'
            end
        ) then true
        else false
    end                                                     as flag_concordancia

from calc
