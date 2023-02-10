from relief_planning import output_schema
from relief_planning import input_schema
import pulp
from pulp import lpSum
import pandas as pd


def get_optimization_data(dat):
    I = list(dat.suppliers['Supplier ID'])
    J = list(dat.relief_camps['Relief Camp ID'])
    K = list(dat.products['Product ID'])
    c = dict(zip(zip(dat.shipping_costs['Supplier ID'], dat.shipping_costs['Relief Camp ID']),
                 dat.shipping_costs['Cost']))
    u = dict(zip(zip(dat.products_suppliers['Product ID'], dat.products_suppliers['Supplier ID']),
                 dat.products_suppliers['Available Qty']))
    d = dict(zip(zip(dat.products_demands['Product ID'], dat.products_demands['Relief Camp ID']),
                 dat.products_demands['Demand Qty']))
    p = {(k, j): 2 * max([c.get((i, j), 0) for i in I]) for k, j in d.keys()}
    x_keys = [(k, i, j) for k in K for i, j in c.keys() if (k, i) in u if (k, j) in d]
    y_keys = [(k, j) for k, j in d.keys()]
    return I, J, K, c, u, d, p, x_keys, y_keys


def solve(dat):
    params = input_schema.create_full_parameters_dict(dat)
    I, J, K, c, u, d, p, x_keys, y_keys = get_optimization_data(dat)

    # Build optimization model
    mdl = pulp.LpProblem('relief_planing', sense=pulp.LpMinimize)

    # Add decision variables
    # Quantity (truckloads) of Product 𝑘 to be shipped from Supplier 𝑖 to Relief Camp 𝑗.
    x = pulp.LpVariable.dicts(indices=x_keys, cat=pulp.LpContinuous, lowBound=0, name='x')
    # Shortfall (truckloads) of Product 𝑘 in Relief Camp 𝑗.
    y = pulp.LpVariable.dicts(indices=y_keys, cat=pulp.LpContinuous, lowBound=0, name='y')

    # Add constraints
    # C1) Demand for Product 𝑘 in Relief Camp 𝑗:
    for k, j in d.keys():
        mdl.addConstraint(lpSum(x[k, i, j] for i in I if (k, i, j) in x_keys) == d[k, j] - y[k, j], name=f'C1_{k}_{j}')

    # C2) Maximum availability of Product 𝑘 at Supplier 𝑖:
    for k, i in u.keys():
        mdl.addConstraint(lpSum(x[k, i, j] for j in J if (k, i, j) in x_keys) <= u[k, i], name=f'C2_{k}_{i}')

    # Defining objective function
    # Shipment cost
    shipment = lpSum(c[i, j] * x[k, i, j] for k, i, j in x_keys)
    # Shortfall
    shortfall = lpSum(p[k, j] * y[k, j] for k, j in y_keys)
    # Set objective function
    mdl.setObjective(shipment + shortfall)

    # Optimize and retrieve the solution
    if params['Solver'] == 'CBC':
        mdl.solve(pulp.PULP_CBC_CMD(timeLimit=params['Time Limit'], gapRel=params['MIP Gap']))
    elif params['Solver'] == 'Gurobi PuLP':
        mdl.solve(pulp.GUROBI_CMD(timeLimit=params['Time Limit'], gapRel=params['MIP Gap']))
    else:
        raise ValueError(f"Bad value for parameter solver: {params['Solver']}")

    status = pulp.LpStatus[mdl.status]
    if status == 'Optimal':
        x_sol = [(k, i, j, var.value()) for (k, i, j), var in x.items() if var.value() > 1e-4]
        y_sol = [(k, j, var.value()) for (k, j), var in y.items() if var.value() > 1e-4]
        print(f'Shipment Cost: {shipment.value()}')
        print(f'Shortfall Penalty: {shortfall.value()}')
    else:
        x_sol, y_sol = None, None
        print(f'Model is not optimal. Status: {status}')

    sln = output_schema.PanDat()
    # Populating the output schema

    if x_sol and y_sol:
        # Populate the shipments table
        shipments_df = pd.DataFrame(x_sol, columns=[
            'Product ID', 'Supplier ID', 'Relief Camp ID', 'Shipped Qty'])
        shipments_df = shipments_df.merge(dat.products[['Product ID', 'Product Name']],
                                          on='Product ID', how='left')
        shipments_df = shipments_df.merge(dat.suppliers[['Supplier ID', 'Supplier Name']],
                                          on='Supplier ID', how='left')
        shipments_df = shipments_df.merge(dat.relief_camps[['Relief Camp ID', 'Relief Camp Name']],
                                          on='Relief Camp ID', how='left')
        shipments_df = shipments_df.round({'Shipped Qty': 2})
        shipments_df = shipments_df.astype({'Shipped Qty': 'float64'})
        sln.shipments = shipments_df[['Product ID', 'Supplier ID', 'Relief Camp ID',
                                      'Product Name', 'Supplier Name', 'Relief Camp Name', 'Shipped Qty']]
        # Populate the shortfalls table
        shortfalls_df = pd.DataFrame(y_sol, columns=['Product ID', 'Relief Camp ID', 'Shortfall Qty'])
        shortfalls_df = shortfalls_df.merge(dat.products[['Product ID', 'Product Name']],
                                            on='Product ID', how='left')
        shortfalls_df = shortfalls_df.merge(dat.relief_camps[['Relief Camp ID', 'Relief Camp Name']],
                                            on='Relief Camp ID', how='left')
        shortfalls_df = shortfalls_df.round({'Shortfall Qty': 2})
        shortfalls_df = shortfalls_df.astype({'Shortfall Qty': 'float64'})
        sln.shortfalls = shortfalls_df[['Product ID', 'Relief Camp ID',
                                        'Product Name', 'Relief Camp Name', 'Shortfall Qty']]
    return sln
