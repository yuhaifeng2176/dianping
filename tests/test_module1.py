import unittest
from project_name.module1 import some_function

class TestModule1(unittest.TestCase):

    def test_some_function(self):
        result = some_function()
        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()
