-- Camada de Qualidade (4/4): relatorio detalhado por regra -- quantos
-- registros falharam em cada uma das 9 regras de validacao, na ultima
-- execucao. Grao = regra.

with validados as (

    select * from {{ ref('formularios_validados') }}

)

select 'id_formulario_valido' as regra, 'Formato UUID valido' as descricao,
       sum(case when not chk_id_formulario_valido then 1 else 0 end) as total_falhas
from validados

union all

select 'id_internacao_preenchido', 'ID da internacao preenchido',
       sum(case when not chk_id_internacao_preenchido then 1 else 0 end)
from validados

union all

select 'id_paciente_preenchido', 'ID do paciente preenchido',
       sum(case when not chk_id_paciente_preenchido then 1 else 0 end)
from validados

union all

select 'data_avaliacao_valida', 'Data de avaliacao presente e valida',
       sum(case when not chk_data_avaliacao_valida then 1 else 0 end)
from validados

union all

select 'hospital_preenchido', 'Hospital preenchido',
       sum(case when not chk_hospital_preenchido then 1 else 0 end)
from validados

union all

select 'estado_atual_valido', 'Estado atual dentro do dominio (UTI/Semi-UTI/Enfermaria/Home Care)',
       sum(case when not chk_estado_atual_valido then 1 else 0 end)
from validados

union all

select 'direcao_transicao_valida', 'Direcao dentro do dominio (Manter/Desescalonar/Escalonar)',
       sum(case when not chk_direcao_transicao_valida then 1 else 0 end)
from validados

union all

select 'pontuacao_seguranca_valida', 'Pontuacao de seguranca entre 0 e 10',
       sum(case when not chk_pontuacao_seguranca_valida then 1 else 0 end)
from validados

union all

select 'criterios_preenchidos', 'Criterios de seguranca/alerta preenchidos',
       sum(case when not chk_criterios_preenchidos then 1 else 0 end)
from validados
