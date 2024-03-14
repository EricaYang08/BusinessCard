from re import L
import string
import sys
import json

#Wenhui Yang 01/25/2022
# check if the input string is an email
def is_email(str):
    str_length = len(str)
    for i in range(str_length):
        if(str[i]== "@"):
            return 1
    return 0

#Wenhui Yang 03/28 /2022
# check if the input string is a phone number
def is_phone_num(str):
    str_length = len(str)
    count_num = 0
    for i in range(str_length):
        if(str[i].isnumeric() == True):
            count_num = count_num + 1
    if(count_num <= 5):
        return 0
    count_char = 0
    for i in range(str_length): 
        if(str[i].isalpha() == True):
            count_char = count_char + 1
    if(count_char == 0):
        return 1
    if(count_char > 0):
       sub_str = str[0:3]
       if "f" in sub_str:
           return 0
       elif "a" in sub_str:
           return 0
       elif "x" in sub_str:
            return 0
       elif "F" in sub_str:
            return 0
       elif "A" in sub_str:
            return 0
       elif "X" in sub_str:
            return 0
       else:
           return 1
        
    return 0

# 03/28/2022 Wenhui Yang
# get the phone number from input string without prefix
def get_phone_num(str):
    phone_num = ""
    if("+1" in str):
        str = str.replace("+1","",1)
    if(("(" or ")") in str):
        str = str.replace("(","")
        str = str.replace(")","")
    index = []
    str_num = 0
    for i in range(len(str)):
        if(str[i].isalpha() == True):
            str_num = str_num + 1
    if(str_num >= 2):
        for i in range(len(str)):
            if((str[i] == " ") or (str[i] == ":")):
                index.append(i)
    if(len(index) >= 2):
        phone_num += str[index[0]:len(str)]
    else:
        phone_num += str[0:len(str)]
    return phone_num

# 01/31/2022 Wenhui Yang
# check if the input string is a fax number
def is_fax_num(str):
    str_length = len(str)
    count_num = 0
    for i in range(str_length):
        if(str[i].isnumeric() == True):
            count_num = count_num + 1
    if(count_num <=5):
        return 0
    elif(is_phone_num(str) == 1):
        return 
    sub = str[0:3]
    if "f" in sub:
        return 1
    if "F" in sub:
        return 1
    else:
        return 0 

# 01/25/2022 Wenhui Yang
# get the email from input string without prefix
def get_email(str):
    email = ""
    count = 0
    for i in range(len(str)):
        if((str[i].isnumeric() == False) and (str[i].isalpha()==False) and (str[i] != ".") and (str[i] != "@")):
            if(count < i):
                count = i
    for i in range(len(str)):
        if(count < i):
            email = email + str[i]
    return email

#02/08/2022
def get_fax_num(str):
    fax_num = ""
    if("+1" in str):
        str = str.replace("+1","",1)
    if(("(" or ")") in str):
        str = str.replace("(","")
        str = str.replace(")","")
    index = []
    for i in range(len(str)):
      if((str[i] == " ") or (str[i] == ":")):
        index.append(i)
    fax_num += str[index[0]:len(str)-1]
    return fax_num

# 01/31/2022 Wenhui Yang
# check if the input string is an address  
def is_address(str):
    count_num = 0
    for i in range(len(str)):
        if(str[i].isnumeric() == True):
            count_num = count_num + 1
    if((count_num > 2) and (is_phone_num(str) == 0) and (is_fax_num(str) == 0)):
        return 1
    return 0

# main classification method that output the result and return as a json object
def classification(input_str,height):
  #03/28/2022 Wenhui Yang
  length = len(input_str) 
  output = {}
  char_num = []
  num_num = []
  num_count = 0
  for i in range(length):
      for j in range(len(input_str[i])):
          if(input_str[i][j].isnumeric() == True):
             num_count = num_count + 1
      char_num.append(len(input_str[i]))
      num_num.append(num_count)
      num_count = 0

  #use character density to find number and fax number which character density = number of number character/ total character
  # find the two largest character density which should be either fax or phone
  character_density = []
  for i in range(len(char_num)):
      character_density.append(num_num[i] / char_num[i])
  large_1 = max(character_density)
  large1_index = character_density.index(large_1)
  character_density2 = character_density
  character_density2.pop(large1_index)
  large2_index = max(character_density2)
  large2_index = character_density.index(large2_index)
  #if the string that have the largest character density is larger than 20 which is twice of the digit number or less than 8 since phone number usually have 10 digits so we give 2 digits as a tolerant 
  # for low accuracy
  if(len(input_str[large1_index]) > 2*10 or (len(input_str[large1_index]) < 8)):
      large1_index = large2_index
      character_density2.pop(large2_index)
      large2_index = max(character_density2)
      large2_index = character_density.index(large2_index)
  phone_index = 0
  # use prefix of these two string to find which is phone number
  #check string for 0:3 because fax is 3 characters and we give one more tolerant for low accuracy
  prefix_check = input_str[large1_index][0:3]
  if("f" in prefix_check):
      phone_index = large2_index
  elif("a" in prefix_check):
      phone_index = large2_index
  elif("x" in prefix_check):
      phone_index = large2_index
  elif("F" in prefix_check):
      phone_index = large2_index
  elif("A" in prefix_check):
      phone_index = large2_index
  elif("X" in prefix_check):
      phone_index = large2_index
  else:
      phone_index = large1_index
  prefix_num = 0
  # extract the phone number without the prefix
  # check the number of characters in prefix
  temp_index = 0
  while ((input_str[phone_index][temp_index]  != ":") and (input_str[phone_index][temp_index] != " ")):
      temp_index = temp_index + 1
  for i in range(temp_index):
      if(input_str[phone_index][i].isalpha() == True):
          prefix_num = prefix_num + 1
  #if we detect less than half of the prefix as characters, we will think that 1 character could be mistake from recognition which should be number originally
  if(prefix_num  > temp_index / 2):
      output["Phone Number"] = get_phone_num(input_str[phone_index])
  else:
      output["Phone Number"] = input_str[phone_index]

#02/15/2022 Wenhui Yang
# we find the largest font size and classified this as a person name.
  current_height = 0
  current_index = 0
  for i in range(length):
      current_index = input_str.index(input_str[i])
      if(current_height < height[current_index] and ((input_str[i][0].isalpha() == True) or (input_str[i][0].isnumeric() == True))):
          current_height = height[current_index]
  current_index = height.index(current_height)
  output["Person Name"] = input_str[current_index] 


  json_output = {}
  json_output["Phone Number"] = output["Phone Number"]
  json_output["Person Name"] = output["Person Name"]
  json_string = json.dumps(json_output)
  print(json_output)
  return json_string

classification(input_str,height)  
