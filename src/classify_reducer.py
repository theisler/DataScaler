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
  results = {}

  
  try:
    line = reader.readline()
    while line:
      words = prep_line(line)
      (col_name, col_type) = extract_key_value(words)
      
      record_values(results, col_name, col_type)
      
      line = reader.readline()
  except "end of file":
    None

  return results


def write_results(results):
  try:
    for result in results:
      print str(result) + "\t" + str(results[result])
  except:
    sys.stderr.write("Unexpected error")
    raise

def prep_line(line):
  line = line.strip()
  words = line.split('\t')
  return words

def extract_key_value(words):
  return (words[0], words[1])

def record_values(values, col_name, col_type):
  if col_type != 'U':
    if col_name in values:
      if values[col_name] == 'N' and col_type == 'T':
        values.update({col_name:col_type})
      #else:
      #  None
    else:
      values.update({col_name:col_type})
    
  

if __name__ == "__main__": 
  main(sys.argv) 
