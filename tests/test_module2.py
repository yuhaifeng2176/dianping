import unittest
from project_name.module2 import another_function

class TestModule2(unittest.TestCase):

    def test_another_function(self):
        result = another_function()
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
