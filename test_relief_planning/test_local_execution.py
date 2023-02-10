import relief_planning
import unittest
import utils


class TestLocalExecution(unittest.TestCase):
    """
    THIS IS NOT UNIT TESTING! Unit testing are implemented in other scripts.

    This class only serves the purpose of conveniently (with one click) executing solve engines locally during
    development.

    In addition, the methods in this class mimic the execution flow that a user typically experience on a Mip Hub app.
    """

    def test_1_action_data_ingestion(self):
        dat = utils.read_data('inputs/testing_data.xls', relief_planning.input_schema)
        utils.check_data(dat, relief_planning.input_schema)
        utils.write_data(dat, 'inputs', relief_planning.input_schema)

    def test_2_main_solve(self):
        dat = utils.read_data('inputs', relief_planning.input_schema)
        sln = relief_planning.solve(dat)
        utils.write_data(sln, 'outputs', relief_planning.output_schema)


if __name__ == '__main__':
    unittest.main()
