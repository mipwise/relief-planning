__version__ = "0.1.0"
from relief_planning.schemas import input_schema, output_schema
from relief_planning.main import solve

# For a configured deployment on Mip Hub see:
# https://github.com/mipwise/mip-go/tree/main/6_deploy/4_configured_deployment

input_tables_config = {
    'hidden_tables': ['parameters'],
    'categories': {
        'Master Data': ['products', 'suppliers', 'relief_camps'],
        'Supply and Demand': ['products_suppliers', 'products_demands']
    },
    'order': [],
    'tables_display_names': {},
    'columns_display_names': {},
    'hidden_columns': {}
    }

output_tables_config = {
    'hidden_tables': [],
    'categories': {},
    'order': [],
    'tables_display_names': {},
    'columns_display_names': {},
    'hidden_columns': {}
    }
