str1 = "Mary"
str2 = "Mark"
if str1 == str2:
    print(f'"{str1}" and "{str2}" are equal.')
else:
    print(f'"{str1}" and "{str2}" are not equal.')
if str1 < str2:
    print(f'"{str1}" come before "{str2}" in lexicographical order.')
elif str1 > str2:
        print(f'"{str1}" come after "{str2}" in lexicographical order.')
if str1.lower() == str2.lower():
     print(f'"{str1}" and "{str2}" are equal when case is ignored.')
else:
      print(f'"{str1}" and "{str2}" are not equal when case is ignored.')