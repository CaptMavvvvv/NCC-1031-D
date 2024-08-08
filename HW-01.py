def format_strings(args):
    if len(args) == 1:
        return args[0].replace(' ', '-').upper()

    result = ''.join(args).upper()
    return result

if __name__ == '__main__':
  result = format_strings("Hello", "world", "this", "is", "a", "test")
  print(result)  # Output: HELLOWORLDTHISISATEST

  result = format_strings("Python", "is", "fun")
  print(result)  # Output: PYTHONISFUN

  result = format_strings("Hello World")
  print(result)  # Output: HELLO-WORLD
