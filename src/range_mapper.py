#!/usr/bin/python
import sys
import csv

def get_csv_reader(input_file):
  csv_reader = csv.reader(input_file, delimiter=',', quotechar='"')
  return csv_reader


def process_header_row(row):
  col_names = []
  for col in row:
    col = str(col).strip()
    col_names.append(col)

  return col_names


def process_row(row, field_types):
  cnt_col = 0
  for col in row:
    col = col.strip()
    
    if len(col) > 0: # Suppress blank values
      field_type = get_field_type(cnt_col, field_types)
      column_data = extract_column_data(col, field_type)
      output_field_data(cnt_col, field_type, column_data)

    cnt_col += 1
    
  return


def get_field_type(col_num, field_types):
  # Use the type specified in the arguments if available
  if col_num >= 0 and col_num < len(field_types):
    field_type = field_types[col_num]
  else:
    field_type = 'T'
  
  return field_type


def extract_column_data(col, field_type):
  if field_type == 'N':
    retval = extract_numeric(col)
  elif field_type == 'T':
    retval = extract_text(col)
  else:
    retval = extract_unknown(col)

  return retval


def extract_numeric(col_string):
  try:
    retval = float(col_string)
  except:
    retval = 0

  return retval


def extract_text(col_string):
  return col_string.strip()


def extract_unknown(col_string):
  is_numeric = False
  try:
    float(col_string)
    is_numeric = True
  except:
    if len(col_string) == 0:
      is_numeric = True

  if is_numeric:
    return extract_numeric(col_string)
  else:
    return extract_text(col_string)

  

def output_field_data(col_num, field_type, col_data):
  if field_type == 'N':
    output = "Number:" + str(cnt_col) + "\t" + str(col_data)
  else:
    if len(col_data) > 0: # Suppress blank values
      output = "Text:" + str(cnt_col) + "\t" + col_data
    
  print output


def process_args(args):
  options = initialize_options()
  messages= ''

  try:
    cnt = 0
    while cnt < len(args):
      arg = args[cnt].lower()
    
      if arg == '--coltypes':
        cnt += 1
        if cnt < len(args):
          options['field_types'] = args[cnt]
          
      else:
        messages = 'Unknown argument ' + arg + '\n'
      
      cnt += 1

  except:
    messages = 'Unexpected error in process_args\n'

  return (options, messages)


def initialize_options():
  options = { 'field_types':'' }

  return options


def main(argv):
  args = sys.argv[1:]
  (options, messages) = process_args(args)
  if len(messages)>0:
    sys.stderr.write(messages)
    sys.stderr.write('...Processing continues...\n')


  field_types = options['field_types']
  results = initialize_results()
  
  csv_reader = get_csv_reader(sys.stdin)
  cnt_row = 0
  
  try:
    for row in csv_reader:
      if cnt_row == 0:
        headers = process_header_row(row)
      else:
        process_row(row, field_types)

      cnt_row += 1
        
        
  except "end of file":
    return None

if __name__ == "__main__": 
  main(sys.argv) 
