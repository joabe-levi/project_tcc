-- Grao = avaliacao. Junta o indicador calculado com a sequencia real
-- (proxima avaliacao da mesma internacao). E a tabela fonte da camada Ouro.

with indicador as (

    select * from {{ ref('int_formularios_indicador') }}

),

sequencia as (

    select * from {{ ref('int_internacoes_sequencia') }}

)

select

    i.id_formulario,
    i.id_internacao,
    i.id_paciente,
    i.id_profissional,
    i.nome_profissional,
    i.data_avaliacao,
    i.hospital,
    i.estado_atual,
    i.estado_recomendado,
    i.direcao_transicao,
    i.direcao_recomendada_calculada,
    i.flag_concordancia,
    i.total_criterios_favoraveis,
    i.total_criterios_alerta,
    i.pontuacao_seguranca,
    i.justificativa,
    i.data_prevista_transicao,
    i.observacoes,

    s.proximo_estado_real,
    s.data_proxima_avaliacao_real,
    s.transicao_efetivada_real,
    s.horas_ate_proxima_avaliacao

from indicador i
left join sequencia s
    on s.id_formulario = i.id_formulario
