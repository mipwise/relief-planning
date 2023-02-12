import relief_planning
import unittest
import os
import utils


class TestMipMe(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        dat = utils.read_data(os.path.join('testing_data', 'testing_data.json'), relief_planning.input_schema)
        cls.params = relief_planning.input_schema.create_full_parameters_dict(dat)
        cls.dat = dat

    def test_1_action_data_ingestion(self):
        utils.check_data(self.dat, relief_planning.input_schema)

    def test_2_main_solve(self):
        sln = relief_planning.solve(self.dat)
        self.assertAlmostEqual(sln.shipments['Shipped Qty'].sum() + sln.shortfalls['Shortfall Qty'].sum(),
                               self.dat.products_demands['Demand Qty'].sum(), 1e-4)
        # TODO: implement more test cases


if __name__ == '__main__':
    unittest.main()
