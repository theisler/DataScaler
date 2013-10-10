import classify_mapper
import unittest

class TestClassifyMapper(unittest.TestCase):
  def SetUp(self):
    reset_data()

  def reset_data(self):
    return

  def test_get_csv_reader1(self):
    input_data = ['a,b,c', '1,2,"a"', '3, 4, "c"']
    csv_reader = classify_mapper.get_csv_reader(input_data)

  
