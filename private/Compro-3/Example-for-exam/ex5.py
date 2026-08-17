def word_frequency(text:str) -> dict:
    result = {}
    spectail = ("!", ",", ".", "/", "'", '"', "")
    for i in spectail:
        text = text.replace(i, '')
        text_split = text.split()
    for b in text_split:
        if b.lower() in result:
            result[b.lower()] += 1
        else:
            result[b.lower()] = 1
    return result

print(word_frequency("Hello world! Hello everyone."))
print(word_frequency("This is a test. This test is easy."))
print(word_frequency("Python is fun. Fun fun fun!"))
print(word_frequency("One word, one word."))