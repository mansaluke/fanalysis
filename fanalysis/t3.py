import re

string = "p = input('How many {} would you like to generate? '.format(freq))"
freq=""
desired_output = "p = ('How many "+freq+" would you like to generate? ')"


str =  "p = input('s  How many {} would you like to generate? '.format(freq))"
rgx = re.compile("(\W+[\w']*\w|\w)")
x = rgx.findall(str)

print(x)


def match_text(text, firstoccuranceonly = False):
    match = (a for a, r in enumerate(x) if text in r)
    if firstoccuranceonly ==False:
        matches = [] #if none found
        matches = list(match)
        return matches
    else: 
        return(next(match))


match_input = match_text("input", True)
match_sym = match_text("{}")
match_format = match_text(".format", True)

for i in x[match_input+1:match_format+1]:
    print(i)

    if i == x[match_format]:
        print(i.replace(".format", ""))
        new_word = i.replace(".format", "")
        x[match_format] = new_word

print(x)
print(''.join(x))

vars = x[match_format+1:]
#vars[1] = vars[1].replace("(", "")
print(vars)
