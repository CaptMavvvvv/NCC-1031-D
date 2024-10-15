def find_multiples_of_three(start: int, end: int) -> list:
    result = []
    if start > end:
      return result
   
    for i in range(start, end + 1):
      if i % 3 == 0:
         result.append(i)

    return result