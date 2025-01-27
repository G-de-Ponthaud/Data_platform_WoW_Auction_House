
 with 
    get_data as (
        SELECT  *,
        NULL as error_columns
        FROM {{ ref("deserialization") }}
    ),
    test_values as (
        SELECT
            {{ test_type("auction_id", 'BIGINT') }},
            {{ test_type_nullable("bid", 'BIGINT') }},
            {{ test_type("item_id", 'BIGINT') }},
            {{ test_type_nullable("pet_breed_id", 'INTEGER') }},
            {{ test_type_nullable("pet_level", 'INTEGER') }},
            {{ test_type_nullable("pet_quality_id", 'INTEGER') }},
            {{ test_type_nullable("pet_species_id", 'INTEGER') }},
            {{ test_type("buyout", 'BIGINT') }},
            {{ test_type("quantity", 'INTEGER') }},
            {{ test_type("time_left", 'VARCHAR(7)') }},
            histo_datetime
        FROM get_data
    )
select *
FROM test_values
