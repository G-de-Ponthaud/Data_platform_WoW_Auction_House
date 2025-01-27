
{% set columns_to_check = dbt_utils.get_filtered_columns_in_relation(from=ref('cast_values'), except=["histo_datetime"]) %}


with get_source as(
    SELECT * 
    FROM {{ ref('cast_values') }}
    ),
    cast_data as(
    SELECT
        CAST(auction_id AS BIGINT) AS auction_id,
        CAST(bid AS BIGINT) AS bid,
        CAST(item_id AS BIGINT) AS item_id,
        CAST(pet_breed_id AS INTEGER) AS pet_breed_id,
        CAST(pet_level AS INTEGER) AS pet_level,
        CAST(pet_quality_id AS INTEGER) AS pet_quality_id,
        CAST(pet_species_id AS INTEGER) AS pet_species_id,
        CAST(buyout AS BIGINT) AS buyout,
        CAST(quantity AS INTEGER) AS quantity,
        CAST(time_left AS VARCHAR(7)) AS time_left,
        histo_datetime
    FROM get_source
    WHERE 
        {% for column in columns_to_check %}
            ({{ column }} IS NULL OR {{ column }} NOT LIKE 'error')
            {% if not loop.last %} AND {% endif %}
        {% endfor %}
    )
    
select *
from cast_data
