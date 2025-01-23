{% macro test_type_nullable(column_name, target_type) %} 
    iff(
        {{column_name}} IS NULL,
        NULL,
        iff(
            TRY_CAST (TO_CHAR({{column_name}}) AS {{ target_type }}) IS NOT NULL,
            TO_CHAR({{ column_name }}),
            'error'
        )
    ) as {{ column_name }}
{% endmacro %}

