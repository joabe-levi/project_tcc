-- Indicador de economia de gastos: quando uma transicao de "Desescalonar" e
-- de fato efetivada (o paciente saiu do nivel mais caro na avaliacao
-- seguinte), estima-se a economia com base no custo diario de referencia
-- (seed_custo_diario_leito) e no tempo ate a proxima avaliacao.
--
-- Grao = avaliacao, mas so linhas com economia > 0 tem valor de negocio;
-- as demais ficam com economia_estimada_brl = 0.
--
-- NOTA: custo_diario_brl e uma estimativa de referencia (ver seed), nao uma
-- tabela de precos real. O indicador serve para demonstrar o *potencial* de
-- economia da ferramenta, nao um valor financeiro auditado.

with avaliacoes as (

    select * from {{ ref('prata_avaliacoes') }}

),

custos as (

    select * from {{ ref('seed_custo_diario_leito') }}

),

calc as (

    select

        a.id_formulario,
        a.id_internacao,
        a.hospital,
        a.nome_profissional,
        a.data_avaliacao,
        a.estado_atual,
        a.proximo_estado_real,
        a.direcao_transicao,
        a.transicao_efetivada_real,
        a.horas_ate_proxima_avaliacao,

        c_atual.custo_diario_brl        as custo_diario_estado_atual,
        c_proximo.custo_diario_brl      as custo_diario_proximo_estado,

        greatest(a.horas_ate_proxima_avaliacao / 24.0, 0) as dias_estimados

    from avaliacoes a
    left join custos c_atual
        on c_atual.estado = a.estado_atual
    left join custos c_proximo
        on c_proximo.estado = a.proximo_estado_real

)

select

    id_formulario,
    id_internacao,
    hospital,
    nome_profissional,
    data_avaliacao,
    estado_atual,
    proximo_estado_real,
    direcao_transicao,
    transicao_efetivada_real,
    custo_diario_estado_atual,
    custo_diario_proximo_estado,
    round(dias_estimados, 2) as dias_estimados,

    case
        when direcao_transicao = 'Desescalonar'
            and transicao_efetivada_real
            and custo_diario_estado_atual is not null
            and custo_diario_proximo_estado is not null
            and custo_diario_estado_atual > custo_diario_proximo_estado
        then round((custo_diario_estado_atual - custo_diario_proximo_estado) * dias_estimados, 2)
        else 0
    end as economia_estimada_brl

from calc
