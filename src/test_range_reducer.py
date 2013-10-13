import range_reducer
import unittest

class TestRangeReducer(unittest.TestCase):
  def SetUp(self):
    reset_data()

  def reset_data(self):
    return

  def test_initialize_results1(self):
    results = range_reducer.initialize_results()
    self.assertEqual(2, len(results))
    self.assertTrue('T' in results)
    self.assertTrue('N' in results)
    self.assertFalse('Q' in results)
    self.assertFalse(5 in results)
    self.assertTrue( results['T'] == {} )
    self.assertTrue( results['N'] == {} )
    

  def test_prep_line1(self):
    input_line = "a\tb"
    prep_result = ["a", "b"]
    
    words = range_reducer.prep_line(input_line)
    self.assertEqual(words, prep_result)


  def test_prep_line2(self):
    input_line = "Number:0\t5.384|1.034e8"
    prep_result = ["Number:0", "5.384|1.034e8"]
    
    words = range_reducer.prep_line(input_line)
    self.assertEqual(words, prep_result)


  def test_extract_key_value1(self):
    input_line = 'Number:0\t1|2'
    expected_result = ('0', 'N', (1, 2))

    words = range_reducer.prep_line(input_line)
    result = range_reducer.extract_key_value(words)
    self.assertEqual(result, expected_result)

    
  def test_extract_key_value2(self):
    input_line = 'Number:0\t5.384|1.034e8'
    expected_result = ('0', 'N', (5.384, 103400000))

    words = range_reducer.prep_line(input_line)
    result = range_reducer.extract_key_value(words)
    self.assertEqual(result, expected_result)


  def test_extract_key_value3(self):
    input_line = 'Number:35\t-5.384|-1.034e8'
    expected_result = ('35', 'N', (-5.384, -103400000))

    words = range_reducer.prep_line(input_line)
    result = range_reducer.extract_key_value(words)
    self.assertEqual(result, expected_result)


  def test_extract_key_value4(self):
    input_line = 'Number:35\t -5.384 | -1.034e8  '
    expected_result = ('35', 'N', (-5.384, -103400000))

    words = range_reducer.prep_line(input_line)
    result = range_reducer.extract_key_value(words)
    self.assertEqual(result, expected_result)


  def test_extract_key_value5(self):
    input_line = 'Text:99\tabbot & costello'
    expected_result = ('99', 'T', 'abbot & costello')

    words = range_reducer.prep_line(input_line)
    result = range_reducer.extract_key_value(words)
    self.assertEqual(result, expected_result)


  def test_extract_key_value6(self):
    input_line = 'Text:433\tabbot &amp; costello'
    expected_result = ('433', 'T', 'abbot &amp; costello')

    words = range_reducer.prep_line(input_line)
    result = range_reducer.extract_key_value(words)
    self.assertEqual(result, expected_result)

  def test_record_values1(self):
    input_line = 'Number:0\t1|2'
    expected_result = {'N': {}, 'T':{}}
    expected_result['N'].update( {'0': (1.0, 2.0)} )

    results = range_reducer.initialize_results()
    words = range_reducer.prep_line(input_line)
    (col_name, col_type, values) = range_reducer.extract_key_value(words)
    range_reducer.record_values(results, col_name, col_type, values)
    self.assertEqual(results, expected_result)
    

  def test_record_values2(self):
    input_line = 'Number:987\t -432.933 | 104040404 '
    expected_result = {'N': {}, 'T':{}}
    expected_result['N'].update( {'987': (-432.933, 104040404.0)} )

    results = range_reducer.initialize_results()
    words = range_reducer.prep_line(input_line)
    (col_name, col_type, values) = range_reducer.extract_key_value(words)
    range_reducer.record_values(results, col_name, col_type, values)
    self.assertEqual(results, expected_result)
    

  def test_record_values3(self):
    input_line = 'Text:73732\t -432.933 | 104040404 '
    expected_result = {'N': {}, 'T':{}}
    expected_result['T'].update( {'73732': {'-432.933 | 104040404':0}} )

    results = range_reducer.initialize_results()
    words = range_reducer.prep_line(input_line)
    (col_name, col_type, values) = range_reducer.extract_key_value(words)
    range_reducer.record_values(results, col_name, col_type, values)
    self.assertEqual(results, expected_result)


  def test_record_values4(self):
    input_line = 'Text:73732\t -432.933 | 104040404 '
    expected_result = {'N': {}, 'T':{}}
    expected_result['T'].update( {'73732': {'-432.933 | 104040404':0}} )

    results = range_reducer.initialize_results()
    words = range_reducer.prep_line(input_line)
    (col_name, col_type, values) = range_reducer.extract_key_value(words)
    range_reducer.record_values(results, col_name, col_type, values)
    words = range_reducer.prep_line(input_line)
    (col_name, col_type, values) = range_reducer.extract_key_value(words)
    range_reducer.record_values(results, col_name, col_type, values)
    words = range_reducer.prep_line(input_line)
    (col_name, col_type, values) = range_reducer.extract_key_value(words)
    range_reducer.record_values(results, col_name, col_type, values)

    self.assertEqual(results, expected_result)

    
  def test_record_values5(self):
    input_line1 = 'Text:73732\tJack'
    input_line2 = 'Text:2\t -432.933 | 104040404 '
    expected_result = {'N': {}, 'T':{}}
    expected_result['T'].update( {'73732': {'Jack':0}} )
    expected_result['T'].update( {'2': {'-432.933 | 104040404':0}} )

    results = range_reducer.initialize_results()

    words = range_reducer.prep_line(input_line1)
    (col_name, col_type, values) = range_reducer.extract_key_value(words)
    range_reducer.record_values(results, col_name, col_type, values)

    words = range_reducer.prep_line(input_line2)
    (col_name, col_type, values) = range_reducer.extract_key_value(words)
    range_reducer.record_values(results, col_name, col_type, values)
    
    self.assertEqual(results, expected_result)


  def test_record_values6(self):
    input_lines = ['Text:1\tAlpha'
                   , 'Text:1\tBravo'
                   , 'Text:1\tCharlie'
                   , 'Text:2\tAnder'
                   , 'Text:2\tBruno'
                   ]
                   
    expected_result = {'N': {}, 'T':{}}
    expected_result['T'].update( {'1': {'Alpha':0, 'Bravo':0, 'Charlie':0}, '2':{'Ander':0, 'Bruno':0} } )
    results = range_reducer.initialize_results()

    for input_line in input_lines:  
      words = range_reducer.prep_line(input_line)
      (col_name, col_type, values) = range_reducer.extract_key_value(words)
      range_reducer.record_values(results, col_name, col_type, values)

    self.assertEqual(results, expected_result)
    

##  def test_prep_and_extract2(self):
##    input_line = " a\tb "
##    prep_result = ["a", "b"]
##    extract_result = ('a', 'b')
##    
##    words = classify_reducer.prep_line(input_line)
##    self.assertEqual(words, prep_result)
##    self.assertEqual(extract_result, classify_reducer.extract_key_value(words))
##
##
##  def test_prep_and_extract3(self):
##    input_line = " a\tb, c "
##    prep_result = ["a", "b, c"]
##    extract_result = ('a', 'b, c')
##    
##    words = classify_reducer.prep_line(input_line)
##    self.assertEqual(words, prep_result)
##    self.assertEqual(extract_result, classify_reducer.extract_key_value(words))
##
##
##  def test_prep_and_extract4(self):
##    input_line = " a\tb|c|d "
##    prep_result = ["a", "b|c|d"]
##    extract_result = ('a', 'b|c|d')
##    
##    words = classify_reducer.prep_line(input_line)
##    self.assertEqual(words, prep_result)
##    self.assertEqual(extract_result, classify_reducer.extract_key_value(words))
##
##
##  def test_prep_and_extract5(self):
##    input_line = " a\tb,1,2, -3.05 "
##    prep_result = ["a", "b,1,2, -3.05"]
##    extract_result = ('a', 'b,1,2, -3.05')
##    
##    words = classify_reducer.prep_line(input_line)
##    self.assertEqual(words, prep_result)
##    self.assertEqual(extract_result, classify_reducer.extract_key_value(words))
##



if __name__ == '__main__':
    unittest.main()
