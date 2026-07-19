global_var = "I'm outside the function"

def my_func():
    print(global_var)

my_func()

print(global_var)