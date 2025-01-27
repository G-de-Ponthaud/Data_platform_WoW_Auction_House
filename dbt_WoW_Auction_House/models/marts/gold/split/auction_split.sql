
with get_source as (
    select *
    from {{ ref("flat_auction_snapshot") }}
    where DBT_VALID_TO is null AND pet_breed_id IS NOT NULL
),
split_data as (
    select DISTINCT
        source.auction_id as auction_id,
        source.bid as bid,
        source.item_id as item_id,
        pet.pet_id as pet_id,
        source.buyout as buyout,
        source.quantity as quantity,
        source.time_left as time_left
    from get_source source
    LEFT JOIN {{ ref("pet_split") }} pet
    ON source.pet_breed_id = pet.pet_breed_id AND source.pet_level = pet.pet_level AND source.pet_quality_id = pet.pet_quality_id AND source.pet_species_id = pet.pet_species_id
)
select *
from split_data
