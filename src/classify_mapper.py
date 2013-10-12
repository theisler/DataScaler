#!/usr/bin/python
import sys
import csv

def get_csv_reader(input_file):
  csv_reader = csv.reader(input_file, delimiter=',', quotechar='"')
  return csv_reader

def process_header_row(row):
  col_names = []
  for col in row:
    col_names.append(str(col))

  return col_names

def process_row(row):
  cnt_col = 0
  for col in row:
    col = col.strip()
    field_type = get_field_type(col)
    output_field_data(cnt_col, field_type)
    cnt_col += 1
    
  return


def get_field_type(col):
  field_type = 'T'
  if len(col) == 0:
    field_type = 'U' # Type is unknown
  else:
    try:
      v = float(col)
      field_type = 'N' # Type is numeric
    except:
      field_type = 'T' # Type is text
  
  return field_type

def output_field_data(col_num, col_data):
  print str(col_num) + "\t" + col_data


def main(argv):
  csv_reader = get_csv_reader(sys.stdin)
  cnt_row = 0
  
  try:
    for row in csv_reader:
      if cnt_row == 0:
        headers = process_header_row(row)
      else:
        process_row(row)

      cnt_row += 1
        
        
  except "end of file":
    return None

if __name__ == "__main__": 
  main(sys.argv) 
