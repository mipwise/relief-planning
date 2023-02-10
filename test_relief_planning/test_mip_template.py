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
        self.assertSetEqual(set(sln.sample_output_table['Data Field']), {'Option 1', 'Option 2'}, 'Main solve check')


if __name__ == '__main__':
    unittest.main()
