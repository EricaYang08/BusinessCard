from numpy import mean

words = []
#read all words from the first names dataset
with open("names.txt","r") as file:
    for line in file:
        for word in line.split():
            words.append(word)

input_str = "Mark"
val = 0
new_val = 0 
new_index = 0
#find the largest similarity with the names in the list
for i in range(len(words)):
    if(len(words[i]) == len(input_str)):
        for j in range(len(input_str)):
            new_val = mean([input_str[j] == words[i][j]])
            if(val < new_val):
                val = new_val
                new_index = i
print(val)
print(new_index)
print(words[new_index])