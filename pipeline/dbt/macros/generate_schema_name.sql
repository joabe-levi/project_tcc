{#
  Override do macro padrao do dbt: por padrao, quando um model define
  +schema, o dbt concatena "<schema do target>_<schema custom>"
  (ex.: bronze_prata). Aqui queremos o schema custom isolado (bronze/
  prata/ouro), sem prefixo do target.
#}
{% macro generate_schema_name(custom_schema_name, node) -%}
    {%- if custom_schema_name is none -%}
        {{ target.schema }}
    {%- else -%}
        {{ custom_schema_name | trim }}
    {%- endif -%}
{%- endmacro %}
