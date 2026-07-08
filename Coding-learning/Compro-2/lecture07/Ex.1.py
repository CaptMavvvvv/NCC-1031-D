survey_results = [
    ["Python", "JavaScript", "C++"], #Participant 1
    ["Python", "JavaScript", "C#"], #Participant 2
    ["Python", "Java"], #Participant 3
    ["Python", "C++", "JavaScript"], #Participant 4
    ["Python", "JavaScript", "C++", "Java"] #Participant 5
]

languages_sets = [set(numbers) for numbers in survey_results]
#print(languages_sets)

common_languages = set.intersection(*languages_sets)
print("Languages chosen by all participants:", common_languages)

#one_participant = set.(*languages_sets)
print("Languages chosen by only one participant:", one_participant)

unique_languages = (len(languages_sets))
print("Number of unique languages:", unique_languages)

#two_participant = 
print("Languages chosen by exactly two participans:", )

#identical_choice = set.
print("Participants with identical choices:", )