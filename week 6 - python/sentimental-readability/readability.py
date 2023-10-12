import cs50

text = cs50.get_string("Text: ")

letters = 0
sentences = 0
words = 1

for i in range(len(text)):
    if text[i].islower() or text[i].isupper():
        letters += 1
    if text[i] == "." or text[i] == "!" or text[i] == "?":
        sentences += 1
    if text[i] == " ":
        words += 1

l = letters / float(words) * 100
s = sentences / float(words) * 100
grade = round(0.0588 * l - 0.296 * s - 15.8)

if grade < 1:
    print("Before Grade 1")
elif grade >= 16:
    print("Grade 16+")
else:
    print("Grade " + str(grade))
