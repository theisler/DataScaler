import classify_reducer
import unittest

class TestClassifyReducer(unittest.TestCase):
  def SetUp(self):
    reset_data()

  def reset_data(self):
    return

  def test_prep_and_extract1(self):
    input_line = "a\tb"
    prep_result = ["a", "b"]
    extract_result = ('a', 'b')
    
    words = classify_reducer.prep_line(input_line)
    self.assertEqual(words, prep_result)
    self.assertEqual(extract_result, classify_reducer.extract_key_value(words))
    

  def test_prep_and_extract2(self):
    input_line = " a\tb "
    prep_result = ["a", "b"]
    extract_result = ('a', 'b')
    
    words = classify_reducer.prep_line(input_line)
    self.assertEqual(words, prep_result)
    self.assertEqual(extract_result, classify_reducer.extract_key_value(words))


  def test_prep_and_extract3(self):
    input_line = " a\tb, c "
    prep_result = ["a", "b, c"]
    extract_result = ('a', 'b, c')
    
    words = classify_reducer.prep_line(input_line)
    self.assertEqual(words, prep_result)
    self.assertEqual(extract_result, classify_reducer.extract_key_value(words))


  def test_prep_and_extract4(self):
    input_line = " a\tb|c|d "
    prep_result = ["a", "b|c|d"]
    extract_result = ('a', 'b|c|d')
    
    words = classify_reducer.prep_line(input_line)
    self.assertEqual(words, prep_result)
    self.assertEqual(extract_result, classify_reducer.extract_key_value(words))


  def test_prep_and_extract5(self):
    input_line = " a\tb,1,2, -3.05 "
    prep_result = ["a", "b,1,2, -3.05"]
    extract_result = ('a', 'b,1,2, -3.05')
    
    words = classify_reducer.prep_line(input_line)
    self.assertEqual(words, prep_result)
    self.assertEqual(extract_result, classify_reducer.extract_key_value(words))


if __name__ == '__main__':
    unittest.main()
