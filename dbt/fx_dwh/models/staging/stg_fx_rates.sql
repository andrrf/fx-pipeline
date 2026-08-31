with source as (
    
    select * from {{ source('raw', 'fx_rates') }}

),

renamed as (

    select
        rate_date,
        trim(currency) as currency_code,
        multiplier,
        value as raw_value,
        value / multiplier as rate_ron,
        ingested_at

    from source

)

select * from renamed