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
  return words


def write_results(results):
  try:
    sorted_results = sorted(results)
    for result in sorted_results:
      print str(result) + "\t" + str(sorted_results[result])
  except:
    sys.stderr.write("Unexpected error")
    raise

def extract_key_value(words):
  classifier = words[0]
  stuff = classifier.split(':')
  col_name = stuff[1]

  
  value_string = words[1]

  if stuff[0] == 'Number':
    col_type = 'N'
    value = float(value_string)
  else:
    col_type = 'T'
    value = value_string
    
  return (col_name, col_type, value)


def record_values(values, col_name, col_type, value):
  if col_type == 'N':
    num_values =  values['N']
    if col_name in num_values:
      (val_min, val_max) = values[col_name]
      if value < val_min:
        values.update( {col_name:(value, val_max)} )
      elif value > val_max:
        values.update( {col_name:(val_min, value)} )
    else:
      values.update( {col_name:[value, value]} )
  else:
    text_values = values['T']
    if col_name not in values:
      text_values.update( {col_name:{}} )

    values['T'][col_name].update( {value:value} )
    
  return


if __name__ == "__main__": 
  main(sys.argv) 
