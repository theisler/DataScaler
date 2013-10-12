#! /bin/python
# normalize.py

# Normalize a CSV file for MIC (Maximal Information Content) analysis
# Arguments
# --inputFile <path to file>
# --outputFile <path to file>
# --minNumber <number>      Minimum numeric value after scaling. Defaults to 0 (zero)
# --maxNumber <number>      Maximum numeric value after scaling. Defaults to 1000
# --maxEnumerationSize <integer>  Maximum length of an enumeration list. Defaults to 1000



# Three passes are needed
# The first pass determines if each variable is text or numeric
# The second pass determines the ordinal values of the text enumerations,
# and the range of the numeric variables
# The third pass translates the text values into ordinals and
# scales the numeric values


import csv          # CSV files are the main input
import re           # We will use some regular expressions
import sys


# this code is not obvious, hence the comment
# "constant sets up a pattern to handle methods in a class of constants
def constant(f):
  def fset(self, value):
    raise SyntaxError

  def fget(self):
    return f()

  return property(fget, fset)

class _Const(object):
  @constant
  def MIN_OUTPUT_NUMBER():
    return 0

  @constant
  def MAX_OUTPUT_NUMBER():
    return 1000000000
  
  @constant
  def MAX_ENUMERATION_SIZE():
    return 10000

CONST = _Const()


# Global variables
input_file_name = ""
output_file_name = ""
min_output_number = CONST.MIN_OUTPUT_NUMBER
max_output_number = CONST.MAX_OUTPUT_NUMBER
max_enumeration_size = CONST.MAX_ENUMERATION_SIZE



def normalize():
  stage1_determine_types()
  stage2_determine_ranges_and_maps()
  stage3_normalize_data()
  return

def stage1_determine_types():
  csv_reader = open_csv_input_file(input_file_name)

  (col_names, row_types) = determine_types(csv_reader)

  close_csv_input_file(csv_reader)
  
  return


def determine_types(csv_reader):
  row_num = 0
  
  for row in csv_reader:
    if row_num == 0:
      header = row
      col_names = process_header_line(row)
      num_columns = len(col_names)
    else:
      col_num = 0
      for col in row:
        col 

  return (col_names, row_types)

def process_header_row(row):
  col_names = []
  for col in row:
    col_names.append(str(col))
  return col_names
  

def stage2_determine_ranges_and_maps():
  csv_reader = open_csv_input_file(input_file_name)

  read_header(csv_reader)

  process_file_stage1(csv_reader)

  close_csv_input_file(csv_reader)
  
  return


def stage3_normalize_data():
  return


def open_csv_input_file(input_file_name):
#  try:
    csv_file = open(input_file_name, 'rb')
    csv_reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    return csv_reader
#  except IOError:
    
  

def read_header(csv_reader):
  return

def process_file_stage1(csv_reader):
  return

def close_cvs_input_file(csv_reader):
  return

def process_args(args):
  global input_file_name
  global output_file_name
  global min_output_number
  global max_output_number
  global max_enumeration_size

  try:
    cnt = 0
    while cnt < len(args):
      arg = args[cnt]
    
      if arg == "--inputFile":
        cnt += 1
        if cnt < len(args):
          input_file_name = args[cnt]
          
      elif arg == "--outputFile":
        cnt += 1
        if cnt < len(args):
          output_file_name = args[cnt]
          
      elif arg == "--minNumber":
        cnt += 1
        if cnt < len(args):
          min_output_number = int(args[cnt])
          
      elif arg == "--maxNumber":
        cnt += 1
        if cnt < len(args):
          max_output_number = int(args[cnt])
          
      elif arg == "--maxEnumerationSize":
        cnt += 1
        if cnt < len(args):
          max_enumeration_size = args[cnt]

      cnt += 1

    (retval, return_string) = validate_args()

    return (retval, return_string)
  
  except:
    print "Unexpected error:", sys.exc_info()[0]
    print "Processing argument " + str(cnt)
    raise


##def get_next_arg(args, cnt):
##  cnt += 1
##  if cnt < len(args):
##    arg = args[cnt]
##
##  return (arg, cnt)


def validate_args():
  retval = True
  return_string = ""
  
  if len(input_file_name) == 0:
    return_string += "Must have an input file name. Use the --inputFile argument\n"
    retval = False

  if len(output_file_name) == 0:
    return_string += "Must have an output file name. Use the --outputFile argument\n"
    retval = False

  if input_file_name == output_file_name:
    return_string += "Input and output files must be different\n"
    retval = False    

  if min_output_number < CONST.MIN_OUTPUT_NUMBER:
    return_string += "--minNumber must be >= " + str(CONST.MIN_OUTPUT_NUMBER) + "\n"
    retval = False

  if max_output_number > CONST.MAX_OUTPUT_NUMBER :
    return_string += "--maxNumber must be <= " + str(CONST.MAX_OUTPUT_NUMBER) + "\n"
    retval = False

  if max_enumeration_size > CONST.MAX_ENUMERATION_SIZE:
    return_string += "--maxEnumerationSize must be less than " + str(CONST.MAX_ENUMERATION_SIZE) + "\n"
    retval = False

  if (max_output_number <= min_output_number):
    return_string += "--minNumber (" + str(min_output_number) + " must be < --MaxNumber (" + str(max_output_number) + ")\n"
    retval = False

  
  return (retval, return_string)

def print_usage():
  print ""
  print "normalize.py Normalize a CSV file for MIC (Maximal Information Content) analysis:"
  print "Usage: python normalize.py --inputFile <path to file> --outputFile <path to file> --minNumber <integer> --maxNumber <integer> --maxEnumerationSize <integer>"
  print "Where:"
  print "--inputFile is required"
  print "--outputFile is required"
  print "--minNumber (optional) Minimum numeric value after scaling. Defaults to " + str(CONST.MIN_OUTPUT_NUMBER)
  print "--maxNumber (optional) Maximum numeric value after scaling. Defaults to " + str(CONST.MAX_OUTPUT_NUMBER)
  print "--maxEnumerationSize (optional) Maximum length of an enumeration list. Defaults to " + str(CONST.MAX_ENUMERATION_SIZE)
  print ""

# Calls the above functions with interesting inputs.
def main():
  args = sys.argv[1:]
  args.append("--test")
  
  (ok_to_continue, return_string) = process_args(args)
  if not ok_to_continue:
    print return_string
    print_usage()
    sys.exit(1)

  else:
    normalize()


if __name__ == '__main__':
  main()
