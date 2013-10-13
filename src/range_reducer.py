#!/usr/bin/python
import sys 

def main(argv):
  reader = sys.stdin

  try:
    results = extract_data(reader)
    
    write_results(results)
  except:
    sys.stderr.write("Unexpected error")
    raise


def extract_data(reader):
  results = initialize_results()
  
  try:
    line = reader.readline()
    while line:
      words = prep_line(line)
      (col_name, col_type, value) = extract_key_value(words)
      
      record_values(results, col_name, col_type, value)
      
      line = reader.readline()
      
  except "end of file":
    None

  return results


def initialize_results():
  results = {'T':{}, 'N':{}}
  return results


def prep_line(line):
  line = line.strip()
  words = line.split('\t')
  words[0] = words[0].strip()
  words[1] = words[1].strip()
  return words


def write_results(results):
  num_results = results['N']
  text_results = results['T']

  for result in num_results:
    output = format_number_output(result, num_results[result])
    print output

  for result in text_results:
    text_list = text_results[result].keys()
    for value in text_list:
      output = format_text_output(result, value)
      print output


def format_number_output(col_name, value_tuple):
  retval = 'Number:' + str(col_name) + '\t' + str(value_tuple[0]) + '|' + str(value_tuple[1])
  return retval

def format_text_output(col_name, value):
  retval = 'Text:' + str(col_name) + '\t' + value
  return retval
  

def extract_key_value(words):
  key_data = words[0].split(':')
  classifier = key_data[0]
  col_name = key_data[1]

  value_string = words[1]

  if classifier == 'Number':
    col_type = 'N'
    min_max = value_string.split('|')
    value = ( float(min_max[0]), float(min_max[1]) )
  else:
    col_type = 'T'
    value = value_string
    
  return (col_name, col_type, value)


# Numbers are a 2-tuple, text is a single value
def record_values(values, col_name, col_type, value):
  if col_type == 'N':
    num_values =  values['N']

    if col_name not in num_values:
      val_min = value[0]
      val_max = value[1]
    else:
      val_min = num_values[col_name][0]
      val_max = num_values[col_name][1]
      if value[0] < val_min:
        val_min = value[0]
      if value[1] > val_max:
        val_max = value[1]
      
    num_values.update( {col_name:(val_min, val_max)} )
  else:
    text_values = values['T']
    if col_name not in text_values:
      text_values.update( {col_name:{}} )

    text_values[col_name].update( {value:0} )
    
  return


if __name__ == "__main__": 
  main(sys.argv) 
