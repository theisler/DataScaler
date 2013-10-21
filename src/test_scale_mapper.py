import scale_mapper
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
    args = "NTNTUG"
    for cnt in range(len(args)):
      self.assertEqual(args[cnt], scale_mapper.get_field_type(cnt, args))
      

  def test_get_field_type2(self):
    args = "NT"
    for cnt in range(-3, -1):
      self.assertEqual('T', scale_mapper.get_field_type(cnt, args))
      

  def test_get_field_type3(self):
    args = "NT"
    for cnt in range(len(args), len(args)+10):
      self.assertEqual('T', scale_mapper.get_field_type(cnt, args))


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




if __name__ == '__main__':
    unittest.main()
