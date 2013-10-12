import range_mapper
import unittest

class TestRangeMapper(unittest.TestCase):
  def SetUp(self):
    reset_data()

  def reset_data(self):
    return

  def test_process_args1(self):
    args = []
    (options, message) = range_mapper.process_args(args)
    self.assertEqual( options, {'field_types':''} )
    self.assertEqual( message, '' )
    

  def test_process_args2(self):
    args = ['--colTypes', 'TFTNUKK']
    (options, message) = range_mapper.process_args(args)
    self.assertEqual( options, {'field_types':'TFTNUKK'} )
    self.assertEqual( message, '' )
    

  def test_process_args3(self):
    args = ['--COLTYPes', 'ABCDEF', '--verbose']
    (options, message) = range_mapper.process_args(args)
    self.assertEqual( options, {'field_types':'ABCDEF'} )
    self.assertEqual( message, 'Unknown argument --verbose\n' )
    
  def test_process_args4(self):
    args = ['--verbose']
    (options, message) = range_mapper.process_args(args)
    self.assertEqual( options, {'field_types':''} )
    self.assertEqual( message, 'Unknown argument --verbose\n' )
    

  def test_initialize_options1(self):
    options = range_mapper.initialize_options()
    self.assertEqual(options, {'field_types':''})
    

  def test_process_header_row1(self):
    row_data = ['A', 'B', 'C', 'D']
    expected_result = row_data
    result = range_mapper.process_header_row(row_data)
    self.assertEqual(result, expected_result)


  def test_process_header_row2(self):
    # Test stripping white space
    row_data = ['\tA ', 'B\t', 'C ', ' D']
    expected_result = ['A', 'B', 'C', 'D']
    result = range_mapper.process_header_row(row_data)
    self.assertEqual(result, expected_result)


  def test_get_field_type1(self):
    field_types = 'NTNTNTN'
    cnt = 0
    while cnt < len(field_types):
      expected_result = field_types[cnt]
      field_type = range_mapper.get_field_type(cnt, field_types)
      self.assertEqual(field_type, expected_result)
      cnt += 1
      
  
  def test_get_field_type_index_out_of_range1(self):
    field_types = 'NTNTNTN'
    cnt = len(field_types)
    self.assertEqual(range_mapper.get_field_type(cnt, field_types), 'T')


  def test_get_field_type_index_out_of_range2(self):
    field_types = 'NTNTNTN'
    cnt = -1
    self.assertEqual(range_mapper.get_field_type(cnt, field_types), 'T')


  def test_get_field_type_index_out_of_range3(self):
    field_types = 'NTNTNTN'
    cnt = 'A'
    self.assertEqual(range_mapper.get_field_type(cnt, field_types), 'T')


  def test_extract_column_data1(self):
    field_type = 'T'
    value = 'ABC'
    expected_value = value
    retval = range_mapper.extract_column_data(value, field_type)
    self.assertEqual(retval, expected_value)
    

  def test_extract_column_data2(self):
    field_type = 'T'
    value = 'Q,A,A,DD('
    expected_value = value
    retval = range_mapper.extract_column_data(value, field_type)
    self.assertEqual(retval, expected_value)
    

  def test_extract_column_data3(self):
    field_type = 'T'
    value = '\tAB C  '
    expected_value = 'AB C'
    retval = range_mapper.extract_column_data(value, field_type)
    self.assertEqual(retval, expected_value)
    

  def test_extract_column_data4(self):
    field_type = 'N'
    value = '34.5'
    expected_value = 34.5
    retval = range_mapper.extract_column_data(value, field_type)
    self.assertEqual(retval, expected_value)
    

  def test_extract_column_data5(self):
    field_type = 'N'
    value = '34.5e1'
    expected_value = 345
    retval = range_mapper.extract_column_data(value, field_type)
    self.assertEqual(retval, expected_value)


  def test_extract_column_data6(self):
    field_type = 'N'
    value = '-34.5e6'
    expected_value = -34500000.0
    retval = range_mapper.extract_column_data(value, field_type)
    self.assertEqual(retval, expected_value)


  def test_extract_column_data7(self):
    field_type = 'T'
    value = ''
    expected_value = ''
    retval = range_mapper.extract_column_data(value, field_type)
    self.assertEqual(retval, expected_value)


  def test_extract_column_data8(self):
    field_type = 'N'
    value = '  '
    expected_value = 0
    retval = range_mapper.extract_column_data(value, field_type)
    self.assertEqual(retval, expected_value)


  def test_extract_column_data9(self):
    field_type = 'U'
    value = '  '
    expected_value = ''
    retval = range_mapper.extract_column_data(value, field_type)
    self.assertEqual(retval, expected_value)


  def test_extract_column_data10(self):
    field_type = 'X'
    value = '-19.4e3'
    expected_value = -19400
    retval = range_mapper.extract_column_data(value, field_type)
    self.assertEqual(retval, expected_value)



if __name__ == '__main__':
    unittest.main()
