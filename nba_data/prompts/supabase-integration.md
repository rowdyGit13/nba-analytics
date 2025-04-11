# Integrate supabase into streamlit app

## Configure Django Settings

In your Django settings file (usually settings.py), add the Supabase URL and API key as environment variables

## Initialize Supabase Client
Wherever you need to interact with Supabase, initialize the Supabase client:

from supabase import create_client

supabase_url = SUPABASE_URL
supabase_key = SUPABASE_KEY
supabase = create_client(supabase_url, supabase_key)

## Perform Database Operations
Use the supabase client to perform various database operations such as inserting, updating, and querying data. For example:

data = supabase.table('your_table_name').select('*').execute()