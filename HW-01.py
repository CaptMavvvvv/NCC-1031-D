def format_strings(*args):
    result = "".join(args) # Make letters stick together.
    result = result.upper() # Make letters from lower letter to upper letter.
    return result

if __name__ == '__main__':
    result = format_strings("Hello", "world", "this", "is", "a", "test")
    print(result)  # Output: "HELLOWORLDTHISISATEST"

    result = format_strings("Python", "is", "fun")
    print(result)  # Output: "PYTHONISFUN"

    result = format_strings("Concatenate", "these", "strings", "please")
    print(result)  # Output: "CONCATENATETHESESTRINGSPLEASE"