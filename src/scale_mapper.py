#!/usr/bin/python
import csv
import io
import sys


class ScalingData:
  def __init__(self):
    self.min = float(sys.maxint)
    self.max = float(-sys.maxint)
    self.text_list = { '':0 }
    self.scale_type = 'U'

  def get_scale_type(self):
    return self.scale_type

  def set_scale_type(self, new_scale_type):
    if new_scale_type in ['T','N']:
      self.scale_type = new_scale_type
    else:
      raise AttributeError('Attribute value not valid: ' + str(new_scale_type))

  def get_min(self):
    return self.min

  def set_min(self, min_value):
    if min_value < self.min:
      self.min = float(min_value)

  def get_max(self):
    return self.max

  def set_max(self, max_value):
    if max_value > self.max:
      self.max = float(max_value)
  

  def add_text_value(self, text_value):
    text_value = str(text_value)
    if not self.text_list.has_key(text_value):
      self.text_list.update( {text_value:len(self.text_list)} )
    
  def scale(self, value):
    # TODO: Should over-ride as type is set, or create numeric and text sub-classes
    if self.scale_type == 'T':
      return self.scale_text(value)
    elif self.scale_type == 'N':
      return self.scale_number(value)
    else:
      raise AttributeError('Scale type must be initialized')
    

  def scale_default(self, key):
    raise AttributeError('Scale type must be initialized')

  
  def scale_text(self, key):
    key = str(key)
    if self.text_list.has_key(key):
      return self.text_list[key]
    else:
      return 0

  def scale_number(self, value):
    retval = int(round((float(value) - self.min) / (self.max - self.min) * scale_factor,0))
    return retval


  def is_numeric(self, value):
    retval = False
    try:
      f = float(value)
      retval = True
    except:
      retval = False

    return retval


# Global variables
csv_reader = csv.reader
csv_writer = csv.writer
output_buffer = io.BytesIO()
scale_factor = 10000


def get_csv_reader(input_file):
  csv_reader = csv.reader(input_file, delimiter=',', quotechar='"')
  return csv_reader


def get_csv_writer(output_file):
  csv_writer = csv.writer(output_file, quotechar = '"', quoting=csv.QUOTE_MINIMAL)
  return csv_writer


def process_header_row(row):
  col_names = []
  for col in row:
    col = str(col).strip()
    col_names.append(col)

  return col_names


def process_row(row, scalers):
  cnt_col = 0
  results = []
  for col in row:
    col = col.strip()

    if len(col) == 0: # Suppress blank values
      val = None
    else:        
      val = extract_column_data(col, get_field_type(cnt_col, scalers))
      val = scalers[cnt_col].scale(val)

    results.append(val)                
    cnt_col += 1
    
  return results


def get_field_type(col_num, scalers):
  # Check type of scaler
  if col_num >= 0 and col_num < len(scalers):
    field_type = scalers[col_num].get_scale_type()
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
  output = format_output_field_data(col_num, field_type, col_data)
  if len(output) > 0:
    print output


def format_output_field_data(col_label, field_type, col_data):
  output = ""
  
  if field_type == 'N':
    output = "Number:" + str(col_label) + "\t" + str(col_data) + '|' + str(col_data)
  else:
    if len(col_data) > 0: # Suppress blank values
      output = "Text:" + str(col_label) + "\t" + col_data
  return output


def process_args(args):
  options = initialize_options()
  messages= ''

  try:
    cnt = 0
    while cnt < len(args):
      arg = args[cnt].lower()
    
      if arg == '--rangedata':
        cnt += 1
        if cnt < len(args):
          options['rangedata'] = args[cnt]

      elif arg == "--help":
        options.update( {'help':''} )
      
      else:
        messages += 'Unknown argument ' + arg + '\n'
      
      cnt += 1

  except:
    messages = 'Unexpected error in process_args\n'

  return (options, messages)


def initialize_options():
  return { 'rangedata':'' }


def print_help():
  help_text = "scale_mapper.py usage:\n"
  help_text += "\tpython scale_mapper.py --rangedata <file name>" 
  help_text += "\tThe range data file holds the min and max of numeric values" 
  help_text += "\tand an enumerated list of all the text values"
              
  return help_text

def validate_args(options, messages):
  if len(messages) > 0:
    return False
  if len(options['rangedata']) == 0:
    return False
  if options.has_key('help'):
    return False
  
  return True


def read_range_file(file_name):
  results = {}
  f = open(file_name, "r")

  for line in f:
    process_range_file_line(line, results)

  f.close()
  
  return results


def extract_data_from_line(line):
  col_type = ''
  col_name = ''
  value = ''
  
  line = prepare_range_file_line(line)

  line_part = line.split('\t', 1) # Only split at the first \t in case a text value has an embedded \t
  type_col = line_part[0].split(':')

  col_type = type_col[0]
  col_name = int(type_col[1])

  if col_type == 'Text':
    value = line_part[1]
  elif col_type == 'Number':
    text_value = line_part[1].split('|')
    value = [float(text_value[0]), float(text_value[1])]
    
  else:
    raise ValueError('Range file contains an invalid entry: ' + line)
  

  return (col_type, col_name, value)


def process_range_file_line(line, results):
  (record_type, col_name, value) = extract_data_from_line(line)

  if record_type == 'Text':
    if not results.has_key(col_name):
      scaler = ScalingData()
      scaler.set_scale_type('T')
      results.update( {col_name:scaler} )

    scaler = results[col_name]
    scaler.add_text_value(value)
  elif record_type == 'Number':
    if not results.has_key(col_name):
      scaler = ScalingData()
      scaler.set_scale_type('N')
      results.update( {col_name:scaler} )

    scaler = results[col_name]
    scaler.set_min(value[0])
    scaler.set_max(value[1])
    

def prepare_range_file_line(line):
  retval = line.strip()
  return retval


def format_output_line(row_data):
  retval = ""
  return retval


def init_io(input_file, output_file):
  csv_reader = get_csv_reader(input_file)
  csv_writer = get_csv_writer(output_file)
  return (csv_reader, csv_writer)

  
def main(argv):
  global csv_reader
  global csv_writer
  global output_buffer

  
  args = sys.argv[1:]
  (options, messages) = process_args(args)
  if not validate_args(options, messages):
    print help_text()
    exit(1)


  range_file_name = options['rangedata']

  range_data = read_range_file(range_file_name)
  
  # Need to explain slight of hand for output_buffer/stdio
  (csv_reader, csv_writer) = init_io(sys.stdin, sys.stdout)
  
  cnt_row = 0
  
  try:
    for row in csv_reader:
      if cnt_row == 0:
        headers = process_header_row(row)
      else:
        field_data = process_row(row, range_data)
        csv_writer.writerow(field_data) # 

      cnt_row += 1
                
  except "end of file":
    return None


if __name__ == "__main__": 
  main(sys.argv) 
