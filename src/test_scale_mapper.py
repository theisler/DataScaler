import io
import csv
import scale_mapper
import sys
import unittest

class TestScaleMapper(unittest.TestCase):
  def SetUp(self):
    reset_data()

  def reset_data(self):
    return

  def test_process_args1(self):
    args = []
    (options, message) = scale_mapper.process_args(args)
    self.assertEqual( options, {'rangedata':''} )
    self.assertEqual( message, '' )


  def test_process_args2(self):
    args = ['--rangedata']
    (options, message) = scale_mapper.process_args(args)
    self.assertEqual( options, {'rangedata':''} )
    self.assertEqual( message, '' )


  def test_process_args3(self):
    args = ['--rangedata', 'filename']
    (options, message) = scale_mapper.process_args(args)
    self.assertEqual( options, {'rangedata':'filename'} )
    self.assertEqual( message, '' )


  def test_process_args4(self):
    args = ['--rangedata', 'filename', '--verbose']
    (options, message) = scale_mapper.process_args(args)
    self.assertEqual( options, {'rangedata':'filename'} )
    self.assertEqual( message, 'Unknown argument --verbose\n' )


  def test_process_args5(self):
    args = ['--help']
    (options, message) = scale_mapper.process_args(args)
    self.assertEqual( options, {'rangedata':'', 'help':''} )
    self.assertEqual( message, '' )


  def test_process_args6(self):
    args = ['a', 'b', 'c']
    (options, message) = scale_mapper.process_args(args)
    self.assertEqual( options, {'rangedata':''} )
    self.assertEqual( message, 'Unknown argument a\nUnknown argument b\nUnknown argument c\n' )


  def test_validate_args1(self):
    args = []
    (options, message) = scale_mapper.process_args(args)
    self.assertFalse(scale_mapper.validate_args(options, message))
    

  def test_validate_args2(self):
    args = ['--rangedata']
    (options, message) = scale_mapper.process_args(args)
    self.assertFalse(scale_mapper.validate_args(options, message))
    

  def test_validate_args3(self):
    args = ['--rangedata', 'filename']
    (options, message) = scale_mapper.process_args(args)
    self.assertTrue(scale_mapper.validate_args(options, message))
    

  def test_validate_args4(self):
    args = ['--rangedata', 'filename', '--verbose']
    (options, message) = scale_mapper.process_args(args)
    self.assertFalse(scale_mapper.validate_args(options, message))
    

  def test_validate_args5(self):
    args = ['--help']
    (options, message) = scale_mapper.process_args(args)
    self.assertFalse(scale_mapper.validate_args(options, message))
    

  def test_validate_args6(self):
    args = ['a', 'b', 'c']
    (options, message) = scale_mapper.process_args(args)
    self.assertFalse(scale_mapper.validate_args(options, message))


  def test_get_field_type1(self):
    expected_results = "NTNTT"
    scalers = {}
    for cnt in range(len(expected_results)):
      scalers.update( {cnt:scale_mapper.ScalingData()} )
      scalers[cnt].set_scale_type(expected_results[cnt])
    
    for cnt in range(len(expected_results)):
      self.assertEqual(expected_results[cnt], scale_mapper.get_field_type(cnt, scalers))
      

  def test_get_field_type2(self):
    expected_results = "NTNTT"
    scalers = {}
    for cnt in range(len(expected_results)):
      scalers.update( {cnt:scale_mapper.ScalingData()} )
      scalers[cnt].set_scale_type(expected_results[cnt])
    
    for cnt in range(-3, -1):
      self.assertEqual('T', scale_mapper.get_field_type(cnt, scalers))


  def test_get_field_type3(self):
    expected_results = "NTNTT"
    scalers = {}
    for cnt in range(len(expected_results)):
      scalers.update( {cnt:scale_mapper.ScalingData()} )
      scalers[cnt].set_scale_type(expected_results[cnt])
    
    for cnt in range(len(expected_results), len(expected_results)+10):
      self.assertEqual('T', scale_mapper.get_field_type(cnt, scalers))


  def test_extract_column_data1(self):
    field_type = 'T'
    col_in = 'The Rain In Spain]\n'
    col_out = col_in.strip()
    self.assertEqual(col_out, scale_mapper.extract_column_data(col_in, field_type))


  def test_extract_column_data2(self):
    field_type = 'T'
    col_in = 'The Rain\tIn Spain\t'
    col_out = col_in.strip()
    self.assertEqual(col_out, scale_mapper.extract_column_data(col_in, field_type))


  def test_extract_column_data3(self):
    field_type = 'T'
    col_in = 'The Rain\nIn Spain]\t'
    col_out = col_in.strip()
    self.assertEqual(col_out, scale_mapper.extract_column_data(col_in, field_type))


  def test_extract_column_data4(self):
    field_type = 'T'
    col_in = '"The Rain In Spain"'
    col_out = col_in.strip()
    self.assertEqual(col_out, scale_mapper.extract_column_data(col_in, field_type))


  def test_extract_column_data5(self):
    field_type = 'N'
    col_in = '4.5e3'
    col_out = 4500.0
    self.assertEqual(col_out, scale_mapper.extract_column_data(col_in, field_type))


  def test_extract_column_data6(self):
    field_type = 'N'
    col_in = '5'
    col_out = 5.0
    self.assertEqual(col_out, scale_mapper.extract_column_data(col_in, field_type))


  def test_extract_column_data7(self):
    field_type = 'T'
    col_in = '5'
    col_out = '5'
    self.assertEqual(col_out, scale_mapper.extract_column_data(col_in, field_type))


  def test_extract_column_data8(self):
    field_type = 'N'
    col_in = '-8134.314'
    col_out = -8134.314
    self.assertEqual(col_out, scale_mapper.extract_column_data(col_in, field_type))


  def test_extract_column_data9(self):
    field_type = 'U'
    col_in = '-8134.314'
    col_out = -8134.314
    self.assertEqual(col_out, scale_mapper.extract_column_data(col_in, field_type))


  def test_extract_column_data10(self):
    field_type = 'U'
    col_in = '-8134.314ADDD'
    col_out = '-8134.314ADDD'
    self.assertEqual(col_out, scale_mapper.extract_column_data(col_in, field_type))


  def test_process_header_row1(self):
    input_data = ['a', 'b', 'c', 'd']
    output_data = input_data
    self.assertEqual(scale_mapper.process_header_row(input_data), output_data)
  

  def test_process_header_row2(self):
    input_data = [' a', 'b ', ' c ', '\td']
    output_data = ['a', 'b', 'c', 'd']
    self.assertEqual(scale_mapper.process_header_row(input_data), output_data)
  

  def test_process_header_row3(self):
    input_data = ['a\tB', 'b q', 'c   \t', ' d\t  e\n']
    output_data = ['a\tB', 'b q', 'c', 'd\t  e']
    self.assertEqual(scale_mapper.process_header_row(input_data), output_data)


##  def test_process_row1(self):
##    field_types = 'TNTN'
##    scalers = {}
##    for cnt in range(len(field_types)):
##      scalers.update( {cnt:scale_mapper.ScalingData()} )
##      scalers[cnt].set_scale_type(field_types[cnt])
##    
##    input_data = ['ABC', '2.4', '4.59', ' -4.3e3\t\n']
##    output_data = ['ABC', 2.4, '4.59', -4300]
##    self.assertEqual(scale_mapper.process_row(input_data, scalers), output_data)
##    
##
##  def test_process_row2(self):
##    field_types = 'TNTN'
##    input_data = ['ABC', '2.4', '4.59', ' -4.3e3\t\n', 'QA', '1.3']
##    output_data = ['ABC', 2.4, '4.59', -4300, 'QA', '1.3']
##    scalers = {}
##
##    for cnt in range(len(field_types)):
##      scalers.update( {cnt:scale_mapper.ScalingData()} )
##      scalers[cnt].set_scale_type(field_types[cnt])
##
##    self.assertEqual(scale_mapper.process_row(input_data, scalers), output_data)
##    
##
##  def test_process_row3(self):
##    field_types = 'TNTNTNTNTNTN'
##    input_data = ['ABC', '2.4', '4.59', ' -4.3e3\t\n', 'QA', '1.3']
##    output_data = ['ABC', 2.4, '4.59', -4300, 'QA', 1.3]
##    scalers = {}
##
##    for cnt in range(len(field_types)):
##      scalers.update( {cnt:scale_mapper.ScalingData()} )
##      scalers[cnt].set_scale_type(field_types[cnt])
##
##    self.assertEqual(scale_mapper.process_row(input_data, scalers), output_data)


  def test_format_output_line1(self):
    field_data = ['ABC', 2.4, '4.59', -4300, 'QA', 1.3]
    expected_output = 'ABC,2.4,4.59,-4300,QA,1.3'
    output_buffer = io.BytesIO() # Essentially, mocking file output
    csv_writer = scale_mapper.get_csv_writer(output_buffer)
    csv_writer.writerow(field_data)
    self.assertEqual(output_buffer.getvalue().strip(), expected_output)
    

  def test_format_output_line2(self):
    field_data = ['ABC', None, '4.59', -4300, 'QA', 1.3]
    expected_output = 'ABC,,4.59,-4300,QA,1.3'
    output_buffer = io.BytesIO() # Essentially, mocking file output
    csv_writer = scale_mapper.get_csv_writer(output_buffer)
    csv_writer.writerow(field_data)
    self.assertEqual(output_buffer.getvalue().strip(), expected_output)


  def test_extract_data_from_line_numeric1(self):
    input_line = 'Number:3\t4.3|99.33'
    expected_record_type = 'Number'
    expected_col_name = 3
    expected_value = [4.3, 99.33]

    (record_type, col_name, value) = scale_mapper.extract_data_from_line(input_line)
    self.assertEqual(expected_record_type, record_type)
    self.assertEqual(expected_col_name, col_name)
    self.assertEqual(expected_value, value)
    

  def test_extract_data_from_line_numeric2(self):
    input_line = 'Number:3\t4.3|9A.33'
    expected_record_type = 'Number'
    expected_col_name = 3
    expected_value = [4.3, 99.33]

    with self.assertRaises(ValueError):
      (record_type, col_name, value) = scale_mapper.extract_data_from_line(input_line)
    

  def test_extract_data_from_line_numeric3(self):
    input_line = 'Number:3\t4AQ.3|9.33'
    expected_record_type = 'Number'
    expected_col_name = 3
    expected_value = [4.3, 99.33]

    with self.assertRaises(ValueError):
      (record_type, col_name, value) = scale_mapper.extract_data_from_line(input_line)
    

  def test_extract_data_from_text1(self):
    input_line = 'Text:5\tThe rain in Spain'
    expected_record_type = 'Text'
    expected_col_name = 5
    expected_value = 'The rain in Spain'

    (record_type, col_name, value) = scale_mapper.extract_data_from_line(input_line)
    self.assertEqual(expected_record_type, record_type)
    self.assertEqual(expected_col_name, col_name)
    self.assertEqual(expected_value, value)
    

  def test_extract_data_from_text2_tab_in_string(self):
    input_line = 'Text:5\tThe rain in\tSpain'
    expected_record_type = 'Text'
    expected_col_name = 5
    expected_value = 'The rain in\tSpain'

    (record_type, col_name, value) = scale_mapper.extract_data_from_line(input_line)
    self.assertEqual(expected_record_type, record_type)
    self.assertEqual(expected_col_name, col_name)
    self.assertEqual(expected_value, value)
    

  def test_ScalingData_init1(self):
    # Test default construction
    tsd = scale_mapper.ScalingData()
    self.assertEqual(float(sys.maxint), tsd.get_min())
    self.assertEqual(float(-sys.maxint), tsd.get_max())
    self.assertEqual( 0, tsd.scale_text(''))
    self.assertEqual( 0, tsd.scale_text('ABC'))
    self.assertEqual( 0, tsd.scale_text(''))


  def test_ScalingData_is_numeric1(self):
    # Test default construction
    tsd = scale_mapper.ScalingData()
    self.assertTrue(tsd.is_numeric(0))
    self.assertTrue(tsd.is_numeric(1.42))
    self.assertTrue(tsd.is_numeric(-3393939.38383))
    self.assertTrue(tsd.is_numeric(43e19))
    self.assertTrue(tsd.is_numeric('123.456'))
    self.assertTrue(tsd.is_numeric('-18.33e8'))


  def test_ScalingData_is_numeric2(self):
    # Test default construction
    tsd = scale_mapper.ScalingData()
    self.assertFalse(tsd.is_numeric(''))
    self.assertFalse(tsd.is_numeric('AB12'))
    self.assertFalse(tsd.is_numeric('123ABC'))


  def test_ScalingData_scale_type1(self):
    tsd = scale_mapper.ScalingData()
    self.assertEqual('U', tsd.get_scale_type())


  def test_ScalingData_scale_type2(self):
    tsd = scale_mapper.ScalingData()
    tsd.set_scale_type('T')
    self.assertEqual('T', tsd.get_scale_type())
    tsd.set_scale_type('N')
    self.assertEqual('N', tsd.get_scale_type())


  def test_ScalingData_scale_type3(self):
    tsd = scale_mapper.ScalingData()
    with self.assertRaises(AttributeError):
      tsd.set_scale_type('U')
    with self.assertRaises(AttributeError):
      tsd.set_scale_type('V')
    with self.assertRaises(AttributeError):
      tsd.set_scale_type(19)
    with self.assertRaises(AttributeError):
      tsd.set_scale_type({0:0})

  def test_ScalingData_minmax1(self):
    tsd = scale_mapper.ScalingData()
    tsd.set_scale_type('N')
    tsd.set_min(9)
    tsd.set_max(199.0)
    self.assertEqual(9, tsd.get_min())
    self.assertEqual(199, tsd.get_max())


  def test_ScalingData_scale1_not_initialized(self):
    tsd = scale_mapper.ScalingData()
    with self.assertRaises(AttributeError):
      tsd.scale(1)
    with self.assertRaises(AttributeError):
      tsd.scale('A')
   
  def test_ScalingData_scale_int_value(self):
    tsd = scale_mapper.ScalingData()
    scale_type = 'N'
    scale_min = 4
    scale_max = 99
    value_to_scale = 5
    expected_result = int(round((float(value_to_scale) - scale_min) / (scale_max - scale_min)*scale_mapper.scale_factor,0))
    
    tsd.set_scale_type('N')
    tsd.set_min(scale_min)
    tsd.set_max(scale_max)
    self.assertEqual(expected_result, tsd.scale(value_to_scale))
    

  def test_ScalingData_scale_min_max_not_set_int_value(self):
    tsd = scale_mapper.ScalingData()
    scale_type = 'N'
    scale_min = float(sys.maxint)
    scale_max = float(-sys.maxint)
    value_to_scale = 5
    expected_result = int(round((float(value_to_scale) - scale_min) / (scale_max - scale_min)*scale_mapper.scale_factor,0))
    
    tsd.set_scale_type('N')
    tsd.set_min(scale_min)
    tsd.set_max(scale_max)
    self.assertEqual(expected_result, tsd.scale(value_to_scale))


  def test_ScalingData_scale_min_max_not_set_float_value(self):
    tsd = scale_mapper.ScalingData()
    scale_type = 'N'
    scale_min = float(sys.maxint)
    scale_max = float(-sys.maxint)
    value_to_scale = 9.9383393939e14
    expected_result = int(round((float(value_to_scale) - scale_min) / (scale_max - scale_min) * scale_mapper.scale_factor, 0))
    
    tsd.set_scale_type(scale_type)
    tsd.set_min(scale_min)
    tsd.set_max(scale_max)
    self.assertEqual(expected_result, tsd.scale(value_to_scale))


  def test_ScalingData_scale_numeric_string(self):
    tsd = scale_mapper.ScalingData()
    scale_type = 'T'
    value_to_scale = 9.9383393939e14
    
    tsd.set_scale_type(scale_type)
    tsd.add_text_value(value_to_scale)
    
    self.assertEqual(1, tsd.scale(value_to_scale))


  def test_ScalingData_scale_multiple_values(self):
    tsd = scale_mapper.ScalingData()
    scale_type = 'T'
    value_to_scale1 = 9.9383393939e14
    value_to_scale2 = 'ABC'
    
    tsd.set_scale_type(scale_type)
    tsd.add_text_value(value_to_scale1)
    tsd.add_text_value(value_to_scale2)
    
    self.assertEqual(1, tsd.scale(value_to_scale1))
    self.assertEqual(2, tsd.scale(value_to_scale2))


  def test_ScalingData_scale_value_not_in_list(self):
    tsd = scale_mapper.ScalingData()
    scale_type = 'T'
    value_to_scale1 = 9.9383393939e14
    value_to_scale2 = 'ABC'
    value_not_scaled = 'DEF'
    
    tsd.set_scale_type(scale_type)
    tsd.add_text_value(value_to_scale1)
    tsd.add_text_value(value_to_scale2)
    
    self.assertEqual(0, tsd.scale(''))
    self.assertEqual(0, tsd.scale(value_not_scaled))


    
#  def test_initialize_range_file_results(self):
    


if __name__ == '__main__':
    unittest.main()
