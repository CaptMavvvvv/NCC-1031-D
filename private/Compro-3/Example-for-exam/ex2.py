def find_duplicate_chars_count(s: str) -> dict:
    counts = {}
    result = {}
    for char in s:
        if char in counts:
            counts[char] += 1
        else:
            counts[char] = 1

    for char, counts in counts.items():
        if counts > 1:
            result[char] = counts
    return result

print(find_duplicate_chars_count("programming"))
print(find_duplicate_chars_count("mississippi"))
print(find_duplicate_chars_count("abcdefg"))
print(find_duplicate_chars_count("abacabad"))