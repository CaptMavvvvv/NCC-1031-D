def format_strings(args):
    if len(args) == 2:
        result = '-'.join(args)
    else:
        result = ''.join(args)
    result = result.upper()
    return result

if __name__ == '__main__': # Ensures the following code only runs when the script is executed directly
    result = format_strings(["Hello", "world", "this", "is", "a", "test"])
    print(result) # Output: "HELLOWORLDTHISISATEST"

    result = format_strings(["Python", "is", "fun"])
    print(result) # Output: "PYTHONISFUN"

    result = format_strings(["Hello", "world"])
    print(result) # Output: "HELLO- WORLD"