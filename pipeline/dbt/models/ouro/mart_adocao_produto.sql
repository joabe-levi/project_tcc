-- Indicador de produto (comercial): adocao/uso da ferramenta ao longo do
-- tempo. Grao = mes. Serve pra mostrar crescimento de uso, nao qualidade
-- clinica -- e o indicador que sustenta a tese de "produto", nao so de
-- "modelo de dados".

select

    date_trunc('month', data_avaliacao)                as mes,
    count(*)                                            as total_avaliacoes,
    count(distinct hospital)                            as hospitais_ativos,
    count(distinct id_profissional)                     as profissionais_ativos,
    count(distinct id_internacao)                       as internacoes_ativas

from {{ ref('prata_avaliacoes') }}
group by date_trunc('month', data_avaliacao)
order by mes
