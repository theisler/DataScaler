import normalize
import unittest

class TestNormalizeData(unittest.TestCase):
  def SetUp(self):
    reset_data()

  def reset_data(self):
    normalize.input_file_name = ""
    normalize.output_file_name = ""
    normalize.test_flag = False
    normalize.min_output_number = 0
    normalize.max_output_number = 1000
    normalize.max_enumeration_size = 1000
    return

  def test_process_args_input_file_name(self):
    self.reset_data()
    # Input file name only
    input_file_name = ""
    
    args = ["--inputFile", "inputfilename"]
    (ok_to_continue, return_string) = normalize.process_args(args)
    self.assertFalse(ok_to_continue)
    self.assertEqual(normalize.input_file_name, args[1])

  def test_process_args_output_file_name(self):
    self.reset_data()
    # Output file name only    
    input_file_name = ""
    
    args = ["--outputFile", "outputfilename"]
    (ok_to_continue, return_string) = normalize.process_args(args)
    self.assertFalse(ok_to_continue)
    self.assertEqual(normalize.output_file_name, args[1])

  def test_process_args_input_output_file_names(self):
    self.reset_data()
    args = ["--inputFile", "inputfilename", "--outputFile", "outputfilename"]
    (ok_to_continue, return_string) = normalize.process_args(args)
    self.assertTrue(ok_to_continue)
    self.assertEqual(normalize.input_file_name, args[1])
    self.assertEqual(normalize.output_file_name, args[3])

    # Now reverse the order of the arguments    
    self.reset_data()
    args = ["--outputFile", "outputfilename", "--inputFile", "inputfilename"]
    (ok_to_continue, return_string) = normalize.process_args(args)
    self.assertTrue(ok_to_continue)
    self.assertEqual(normalize.input_file_name, args[3])
    self.assertEqual(normalize.output_file_name, args[1])

  def test_process_args_min_output_number(self):
    self.reset_data()
    args = ["--inputFile", "inputfilename", "--outputFile", "outputfilename", "--minNumber", 9]
    (ok_to_continue, return_string) = normalize.process_args(args)
    self.assertTrue(ok_to_continue)
    self.assertEqual(normalize.input_file_name, args[1])
    self.assertEqual(normalize.output_file_name, args[3])
    self.assertEqual(normalize.min_output_number, args[5])

    # number out of range
    self.reset_data()
    args = ["--inputFile", "inputfilename", "--outputFile", "outputfilename", "--minNumber", normalize.CONST.MIN_OUTPUT_NUMBER-1]
    (ok_to_continue, return_string) = normalize.process_args(args)
    self.assertFalse(ok_to_continue)
    self.assertEqual(normalize.input_file_name, args[1])
    self.assertEqual(normalize.output_file_name, args[3])
    self.assertEqual(normalize.min_output_number, args[5])

    # number at border
    self.reset_data()
    args = ["--inputFile", "inputfilename", "--outputFile", "outputfilename", "--minNumber", normalize.CONST.MIN_OUTPUT_NUMBER]
    (ok_to_continue, return_string) = normalize.process_args(args)
    self.assertTrue(ok_to_continue)
    self.assertEqual(normalize.input_file_name, args[1])
    self.assertEqual(normalize.output_file_name, args[3])
    self.assertEqual(normalize.min_output_number, args[5])


#    args = ["test_normalize.py", "--inputFile", "inputfilename", "--outputFile", "outputfilename", "--minNumber", "987", "--maxNumber", "1010"]
  def test_process_args_max_output_number(self):
    self.reset_data()
    args = ["--inputFile", "inputfilename", "--outputFile", "outputfilename", "--maxNumber", 9]
    (ok_to_continue, return_string) = normalize.process_args(args)
    self.assertTrue(ok_to_continue)
    self.assertEqual(normalize.input_file_name, args[1])
    self.assertEqual(normalize.output_file_name, args[3])
    self.assertEqual(normalize.max_output_number, args[5])

    # number out of range
    self.reset_data()
    args = ["--inputFile", "inputfilename", "--outputFile", "outputfilename", "--maxNumber", normalize.CONST.MAX_OUTPUT_NUMBER+1]
    (ok_to_continue, return_string) = normalize.process_args(args)
    self.assertFalse(ok_to_continue)
    self.assertEqual(normalize.input_file_name, args[1])
    self.assertEqual(normalize.output_file_name, args[3])
    self.assertEqual(normalize.max_output_number, args[5])

    # number at border
    self.reset_data()
    args = ["--inputFile", "inputfilename", "--outputFile", "outputfilename", "--maxNumber", normalize.CONST.MAX_OUTPUT_NUMBER]
    (ok_to_continue, return_string) = normalize.process_args(args)
    self.assertTrue(ok_to_continue)
    self.assertEqual(normalize.input_file_name, args[1])
    self.assertEqual(normalize.output_file_name, args[3])
    self.assertEqual(normalize.max_output_number, args[5])

  def test_process_args_min_max_output_number(self):
    self.reset_data()
    args = ["--inputFile", "inputfilename", "--outputFile", "outputfilename", "--minNumber", 9, "--maxNumber", 10]
    (ok_to_continue, return_string) = normalize.process_args(args)
    self.assertTrue(ok_to_continue)
    self.assertEqual(normalize.input_file_name, args[1])
    self.assertEqual(normalize.output_file_name, args[3])
    self.assertEqual(normalize.min_output_number, args[5])
    self.assertEqual(normalize.max_output_number, args[7])

    # max < min
    self.reset_data()
    args = ["--inputFile", "inputfilename", "--outputFile", "outputfilename", "--minNumber", normalize.CONST.MIN_OUTPUT_NUMBER+2, "--maxNumber", normalize.CONST.MIN_OUTPUT_NUMBER+1]
    (ok_to_continue, return_string) = normalize.process_args(args)
    self.assertFalse(ok_to_continue)
    self.assertEqual(normalize.input_file_name, args[1])
    self.assertEqual(normalize.output_file_name, args[3])
    self.assertEqual(normalize.min_output_number, args[5])
    self.assertEqual(normalize.max_output_number, args[7])

    # numbers equal
    self.reset_data()
    args = ["--inputFile", "inputfilename", "--outputFile", "outputfilename", "--minNumber", normalize.CONST.MIN_OUTPUT_NUMBER+3, "--maxNumber", normalize.CONST.MIN_OUTPUT_NUMBER+3]
    (ok_to_continue, return_string) = normalize.process_args(args)
    self.assertFalse(ok_to_continue)
    self.assertEqual(normalize.input_file_name, args[1])
    self.assertEqual(normalize.output_file_name, args[3])
    self.assertEqual(normalize.min_output_number, args[5])
    self.assertEqual(normalize.max_output_number, args[7])

    # number at boundary
    self.reset_data()
    args = ["--inputFile", "inputfilename", "--outputFile", "outputfilename", "--minNumber", normalize.CONST.MIN_OUTPUT_NUMBER, "--maxNumber", normalize.CONST.MAX_OUTPUT_NUMBER]
    (ok_to_continue, return_string) = normalize.process_args(args)
    self.assertTrue(ok_to_continue)
    self.assertEqual(normalize.input_file_name, args[1])
    self.assertEqual(normalize.output_file_name, args[3])
    self.assertEqual(normalize.min_output_number, args[5])
    self.assertEqual(normalize.max_output_number, args[7])


  def test_process_args_enumeration_size(self):
    self.reset_data()
    args = ["--inputFile", "inputfilename", "--outputFile", "outputfilename", "--minNumber", 9, "--maxNumber", 10, "--maxEnumerationSize", normalize.CONST.MAX_ENUMERATION_SIZE]
    (ok_to_continue, return_string) = normalize.process_args(args)
    self.assertTrue(ok_to_continue)
    self.assertEqual(normalize.input_file_name, args[1])
    self.assertEqual(normalize.output_file_name, args[3])
    self.assertEqual(normalize.min_output_number, args[5])
    self.assertEqual(normalize.max_output_number, args[7])



if __name__ == '__main__':
    unittest.main()
  
