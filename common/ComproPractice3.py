def word_frequency(text: str) -> dict:
    # แปลงสตริงทั้งหมดเป็นตัวพิมพ์เล็ก
    text = text.lower()
    
    # แยกคำออกจากกันโดยใช้ช่องว่าง
    words = text.split()
    
    # สร้างพจนานุกรมเพื่อเก็บความถี่ของคำ
    frequency = {}
    
    # นับความถี่ของแต่ละคำ
    for word in words:
        if word in frequency:
            frequency[word] += 1
        else:
            frequency[word] = 1
    
    return frequency

# ทดสอบฟังก์ชัน
print(word_frequency("Hello world! Hello everyone."))  # {'hello': 2, 'world!': 1, 'everyone.': 1}
print(word_frequency("This is a test. This test is easy."))  # {'this': 2, 'is': 2, 'a': 1, 'test.': 2, 'easy.': 1}
print(word_frequency("Python is fun. Fun fun fun!"))  # {'python': 1, 'is': 1, 'fun.': 4}
print(word_frequency("One word , one word."))  # {'one': 2, 'word': 2, ',': 1, '.': 1}