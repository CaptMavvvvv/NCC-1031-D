def divide(a, b):
    try:
        result = a/b
    except ZeroDivisionError as e:
        print(f'Exception: {e}')
    else:
        return result

a,b = map(int, input().split())
print(divide(a,b))
print('End')