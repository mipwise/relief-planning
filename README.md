# Relief Planning
This repository contains a solution developed to support the distribution of 
goods to people impacted by the recent earthquake in Turkey.

The initial mathematical optimization model implemented here recommends the 
quantity of products that should be shipped from each supply location to each 
relief camp (demand points) while minimizing the total shipping cost. Unmet 
demand (due to insufficient supply) is reported as well. 

## Repository guide
- [docs](docs): Hosts documentation (in addition to readme files and docstrings)
  of the project.
- [relief_planning](relief_planning): Contains the Python package that solves the 
  problem.
  It contains scripts that define the input and the output data schemas, the 
  solution engine, and other auxiliary modules.
- [test_relief_planning](test_relief_planning): Hosts testing suits and testing data 
  sets used for testing the solution throughout the development process.
- `pyproject.toml` and `setup.cfg` are used to build the distribution files 
  of the package (more information [here](https://github.com/mipwise/mip-go/blob/main/6_deploy/1_distribution_package/README.md)).