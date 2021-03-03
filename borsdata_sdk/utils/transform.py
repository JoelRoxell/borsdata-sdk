from caseconverter import snakecase

def transform_dict_props_to_lower(d):
  """transforms all props of a dictionary (first level) to lowercase

  Args:
      d (dict): python dict

  Returns:
      dict: new dict with lowercase props
  """
  newDict = {}

  for key, value in d.items():
    newDict[snakecase(key)] = value

  return newDict
