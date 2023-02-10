"""
Defines the input and output schemas of the problem.
For more details on how to implement and configure data schemas see:
https://github.com/mipwise/mip-go/tree/main/5_develop/4_data_schema
"""

from ticdat import PanDatFactory


# region Aliases for datatypes in ticdat
# Remark: use only aliases that match perfectly your needs, otherwise set datatype explicitly
float_number = {
    "number_allowed": True,
    "strings_allowed": (),
    "must_be_int": False,
    "min": -float("inf"),
    "inclusive_min": False,
    "max": float("inf"),
    "inclusive_max": False,
}

non_negative_float = {
    "number_allowed": True,
    "strings_allowed": (),
    "must_be_int": False,
    "min": 0,
    "inclusive_min": True,
    "max": float("inf"),
    "inclusive_max": False,
}

positive_float = {
    "number_allowed": True,
    "strings_allowed": (),
    "must_be_int": False,
    "min": 0,
    "inclusive_min": False,
    "max": float("inf"),
    "inclusive_max": False,
}

integer_number = {
    "number_allowed": True,
    "strings_allowed": (),
    "must_be_int": True,
    "min": -float("inf"),
    "inclusive_min": False,
    "max": float("inf"),
    "inclusive_max": False,
}

non_negative_integer = {
    "number_allowed": True,
    "strings_allowed": (),
    "must_be_int": True,
    "min": 0,
    "inclusive_min": True,
    "max": float("inf"),
    "inclusive_max": False,
}

positive_integer = {
    "number_allowed": True,
    "strings_allowed": (),
    "must_be_int": True,
    "min": 1,
    "inclusive_min": True,
    "max": float("inf"),
    "inclusive_max": False,
}

text = {"strings_allowed": "*", "number_allowed": False}
# endregion

# region INPUT SCHEMA
input_schema = PanDatFactory(
    parameters=[['Name'], ['Value']],  # Do not change the column names of the parameters table!
    products=[['Product ID'], ['Product Name']],
    suppliers=[['Supplier ID'], ['Supplier Name']],
    relief_camps=[['Relief Camp ID'], ['Relief Camp Name']],
    products_suppliers=[['Product ID', 'Supplier ID'], ['Available Qty']],
    shipping_costs=[['Supplier ID', 'Relief Camp ID'], ['Cost']],
    products_demands=[['Product ID', 'Relief Camp ID'], ['Demand Qty']])
# endregion

# region USER PARAMETERS
input_schema.add_parameter('Solver', default_value='CBC', number_allowed=False,
                           strings_allowed=['CBC', 'Gurobi PuLP'])
input_schema.add_parameter('Time Limit', default_value=120, number_allowed=True, strings_allowed=(),
                           must_be_int=False, min=0.0, inclusive_min=True, max=1 * 60 ** 2, inclusive_max=True)
input_schema.add_parameter('MIP Gap', default_value=0.01, number_allowed=True, strings_allowed=(),
                           min=0, inclusive_min=False, max=1, inclusive_max=False)
# endregion

# region OUTPUT SCHEMA
output_schema = PanDatFactory(
    shipments=[['Product ID', 'Supplier ID', 'Relief Camp ID'], [
        'Product Name', 'Supplier Name', 'Relief Camp Name', 'Shipped Qty']],
    shortfalls=[['Product ID', 'Relief Camp ID'], [
        'Product Name', 'Relief Camp Name', 'Shortfall Qty']])
# endregion

# region DATA TYPES AND PREDICATES - INPUT SCHEMA
# region products
table = 'products'
input_schema.set_data_type(table=table, field='Product ID', **text)
input_schema.set_data_type(table=table, field='Product Name', **text)
# endregion

# region suppliers
table = 'suppliers'
input_schema.set_data_type(table=table, field='Supplier ID', **text)
input_schema.set_data_type(table=table, field='Supplier Name', **text)
# endregion

# region relief_camps
table = 'relief_camps'
input_schema.set_data_type(table=table, field='Relief Camp ID', **text)
input_schema.set_data_type(table=table, field='Relief Camp Name', **text)
# endregion

# region products_suppliers
table = 'products_suppliers'
input_schema.set_data_type(table=table, field='Product ID', **text)
input_schema.set_data_type(table=table, field='Supplier ID', **text)
input_schema.set_data_type(table=table, field='Available Qty', **non_negative_float)
input_schema.add_foreign_key(native_table=table, foreign_table='products', mappings=('Product ID', 'Product ID'))
input_schema.add_foreign_key(native_table=table, foreign_table='suppliers', mappings=('Supplier ID', 'Supplier ID'))
# endregion

# region shipping_costs
table = 'shipping_costs'
input_schema.set_data_type(table=table, field='Supplier ID', **text)
input_schema.set_data_type(table=table, field='Relief Camp ID', **text)
input_schema.set_data_type(table=table, field='Cost', **non_negative_float)
input_schema.add_foreign_key(native_table=table, foreign_table='suppliers', mappings=('Supplier ID', 'Supplier ID'))
input_schema.add_foreign_key(native_table=table, foreign_table='relief_camps',
                             mappings=('Relief Camp ID', 'Relief Camp ID'))
# endregion

# region products_demands
table = 'products_demands'
input_schema.set_data_type(table=table, field='Product ID', **text)
input_schema.set_data_type(table=table, field='Relief Camp ID', **text)
input_schema.set_data_type(table=table, field='Demand Qty', **non_negative_float)
input_schema.add_foreign_key(native_table=table, foreign_table='products', mappings=('Product ID', 'Product ID'))
input_schema.add_foreign_key(native_table=table, foreign_table='relief_camps',
                             mappings=('Relief Camp ID', 'Relief Camp ID'))
# endregion

# endregion

# region DATA TYPES AND PREDICATES - OUTPUT SCHEMA
# region shipments
table = 'shipments'
for field in ['Product ID', 'Supplier ID', 'Relief Camp ID', 'Product Name', 'Supplier Name', 'Relief Camp Name']:
    output_schema.set_data_type(table=table, field=field, **text)
output_schema.set_data_type(table=table, field='Shipped Qty', **non_negative_float)
# endregion

# region shortfalls
table = 'shortfalls'
for field in ['Product ID', 'Relief Camp ID', 'Product Name', 'Relief Camp Name']:
    output_schema.set_data_type(table=table, field=field, **text)
output_schema.set_data_type(table=table, field='Shortfall Qty', **non_negative_float)
# endregion
# endregion

