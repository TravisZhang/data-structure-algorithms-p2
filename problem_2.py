import copy
import os

def iter_fun(suffix, path, output):
  if os.path.isfile(path) and path.endswith(suffix):
    output.append(path)
  elif not os.path.isfile(path): 
    # level_list = sorted(os.listdir(path)) 
    level_list = os.listdir(path)
    for i in range(len(level_list)):
      iter_fun(suffix, path + "/" + level_list[i], output)

  pass

def find_files(suffix, path):
  """
  Find all files beneath path with file name suffix.

  Note that a path may contain further subdirectories
  and those subdirectories may also contain further subdirectories.

  There are no limit to the depth of the subdirectories can be.

  Args:
    suffix(str): suffix if the file name to be found
    path(str): path of the file system

  Returns:
     a list of paths
  """
  output = []
  if suffix == "":
    # print(output)
    return output
  base = "." + path
  level_list = sorted(os.listdir(base))
  for i in range(len(level_list)):
    iter_fun(suffix, base + "/" + level_list[i], output)
  # print(output)
  return output

# Test Cases
# print(find_files(".h", ""))
# print(find_files(".c", ""))
# print(find_files(".a", ""))
# print(find_files("", ""))
