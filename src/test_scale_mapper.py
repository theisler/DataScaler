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
    

if __name__ == '__main__':
    unittest.main()
