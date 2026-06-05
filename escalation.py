import tools

def escalation(message):
    print("AN ESCALATION:")
    message = message.rstrip()
    transTable = str.maketrans("GHIJKLMNOPQRSTUVWXYZ0123456789.,?\'\"!/()&:;=+-_$%", "????????????????????????????????????????????????")
    message = message.translate(transTable)


    parts = message.split(" ")

    tools.print_verbose(message)
    firstLetters = []
    for part in parts:
        if len(part) >= 3:
            firstLetters.append(part[0])
            firstLetters.append(part[-5:][0])

    firstLetters.sort()
    firstLetterOccurence = 0

    firstLetter = ""

    for letter in firstLetters:
        if letter != firstLetter and letter != "?" and firstLetters.count(letter) > firstLetterOccurence:
            firstLetter = letter
            firstLetterOccurence = firstLetters.count(letter)

    confidence = firstLetterOccurence / len(firstLetters)

    print("Most likely first letter: " + firstLetter + " : " + str(firstLetterOccurence), " (", round(confidence*100), "%)")

    fives = []
    lastOccurence = -1
    while message.find(firstLetter, lastOccurence+1) != -1:
        fives.append(message[message.find(firstLetter, lastOccurence+1):message.find(firstLetter, lastOccurence+1)+5])
        lastOccurence = message.find(firstLetter, lastOccurence+1)

    fives.sort()
    bestFive = ""
    bestFiveOccurence = 0
    for five in fives:
        if five != bestFive and (not "?" in five) and fives.count(five) > bestFiveOccurence:
            bestFive = five
            bestFiveOccurence = fives.count(five)

    confidence *= bestFiveOccurence / len(fives)
    print("Most likely fives: " + bestFive + " : " + str(bestFiveOccurence), " (", round(confidence*100), "%)")
    print()
    print()
