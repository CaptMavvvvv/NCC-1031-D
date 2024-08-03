def format_strings(args):
    if len(args) == 2: # Check if the number of arguments is exactly two
        result = '-'.join(args) # Join the two arguments with hyphen
    else: # If the number of arguments is not two
        result = ''.join(args) # Join all arguments without any seperators
    result = result.upper() # Turn the resulting string to uppercase
    return result # Return the final uppercase string

if __name__ == '__main__': # Ensures the following code only runs when the script is executed directly
    result = format_strings(["Hello", "world", "this", "is", "a", "test"])
    print(result) # Output: "HELLOWORLDTHISISATEST"

    result = format_strings(["Python", "is", "fun"])
    print(result) # Output: "PYTHONISFUN"

    result = format_strings(["Hello", "world"])
    print(result) # Output: "HELLO- WORLD"