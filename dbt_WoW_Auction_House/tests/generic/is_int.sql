{% test is_int(model, column_name) %}
    select *
    from {{ model }}
    where TRY_CAST({{ column_name }} AS BIGINT) IS NULL
{% endtest %}