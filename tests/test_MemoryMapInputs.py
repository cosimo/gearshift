import unittest

from memoryMapInputs import test_main

class Test_memoryMapInputs(unittest.TestCase):
  def test_memoryMapInputs_main_runs(self):
    # Preliminary test - does main run?
    root = test_main()
    assert root != None



if __name__ == '__main__':
  unittest.main(exit=False)