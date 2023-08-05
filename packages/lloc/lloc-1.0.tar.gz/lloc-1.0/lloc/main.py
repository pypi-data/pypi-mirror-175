import os

def cwis(stroke, word):
  if word in stroke:
    return True
  else:
   return False

def down_str(text, str):
 ok = text
 ko = ok.replace(str, f'\n {str}')
 return ko

def empty_str(file_name):
    with open(file_name) as t:
        lst = [i for i in t.readlines() if '\n' == i]
    return len(lst)


def clear_console():
   os.system('clear')

def right_str(text, str):
 o = text
 k = o.replace(str, f' {str}')
 return k