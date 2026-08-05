'''
The `format_strings` function accepts a variable number of strings using `*args` and performs the following tasks:
1. รวมตัวอักษรทุกตัวเป็น str อันเดียว
2. แปลงทุกตัวเป็น UpperCase
3. แทนที่ช่องว่างทุกช่องด้วย ' - ' '''

def format_strings(*args):
    result = "".join(args) # รวมตัวอักษรทุกตัวไปรวมใน result
    return result.upper().replace(' ', "-") # คืนค่า result ซึ่งมันจะถูกทำให้เป็นพิมพ์ใหญ่และถูกแทนช่องว่างด้วย - 

if __name__ == '__main__':
    result = format_strings("Hello", "world", "this", "is", "a", "test")
    print(result)  # Output: "HELLOWORLDTHISISATEST"

    result = format_strings("Python", "is", "fun")
    print(result)  # Output: "PYTHONISFUN"

    result = format_strings("Hello world")
    print(result)  # Output: "HELLO-WORLD"

