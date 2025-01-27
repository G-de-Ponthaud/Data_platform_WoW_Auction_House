{% macro test_type(column_name, target_type) %}
        iff(
        TRY_CAST (TO_CHAR({{column_name}}) AS {{ target_type }}) IS NOT NULL,
            TO_CHAR({{column_name}}),
            'error'
        ) as {{ column_name }}
{% endmacro %}
