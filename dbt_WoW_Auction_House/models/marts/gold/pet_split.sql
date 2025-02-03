
with get_source as (
    select *
    from {{ ref("flat_auction_snapshot") }}
    where DBT_VALID_TO is null
),
split_data as (
    select DISTINCT
        {{ dbt_utils.generate_surrogate_key(['pet_breed_id', 'pet_level', 'pet_quality_id', 'pet_species_id']) }} as pet_id,
        pet_breed_id,
        pet_level,
        pet_quality_id,
        pet_species_id,
    from get_source 
    WHERE
        pet_breed_id IS NOT NULL
)
select *
from split_data
