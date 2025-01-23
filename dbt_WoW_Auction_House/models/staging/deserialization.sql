
{%- call statement('json_field_list', fetch_result=True) -%}
    select distinct 'item:' || f.path || '::string as ' || lower(replace(f.path, '.', '_')) as select_element
    from
         {{ ref("auction_house_api_snapshot") }},
        lateral flatten(input => item, recursive => true, mode => 'object') f
{%- endcall -%}

{%- set json_field_list = load_result('json_field_list')['data'] -%}

with
    get_source as (select * from {{ ref("auction_house_api_snapshot") }}),
    dynamic_deserialization as (
        select
            id as auction_id,
            {%- for json_field_name in json_field_list %}
                {{ json_field_name[0] }},
            {%- endfor %}
        from get_source
        where dbt_valid_to is null
    ),
    auction_deserialized as (
        select
            source.id as auction_id,
            source.bid as bid,
            deserialisation.id as item_id,
            deserialisation.pet_breed_id as pet_breed_id,
            deserialisation.pet_level as pet_level,
            deserialisation.pet_quality_id as pet_quality_id,
            deserialisation.pet_species_id as pet_species_id,
            source.buyout as buyout,
            source.quantity as quantity,
            source.time_left as time_left,
            source.dbt_valid_from as histo_datetime
        from
            get_source source
            left join dynamic_deserialization deserialisation
                on source.id = deserialisation.auction_id
    )
select *
from auction_deserialized



