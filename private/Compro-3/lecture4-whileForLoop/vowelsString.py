user_string = str(input("Enter the word with string: "))
string_result = ""
vowels = "AEIOU"
for stri in user_string:
    upper_str = stri.upper()
    if upper_str in vowels:
        string_result += "*"
    else:
        string_result += upper_str

print(string_result)