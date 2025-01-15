{{ config(materialized='ephemeral') }}

select 
    Id,
    Bid,
    Item,
    Buyout,
    Quantity,
    Time_Left,
    _AIRBYTE_EXTRACTED_AT as Exctracted_At
from 
    {{ source('sources', 'wow_api') }}