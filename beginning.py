import tools

def beginning(message, stage):
    print("A BEGINNING:")
    import json
    import Levenshtein

    full_message = message
    bestGuess = [0,0,message]

    with open('beginning.json', 'r') as f:
        maps = json.load(f)

    #bestGuess = [0,0,message [0:60]]

    repeats = 3
    for i in range(repeats):
        best = []

        tools.print_verbose("Best guess: ", bestGuess[2])
        tools.print_verbose("Best guess length: ", len(bestGuess[2]))
        tools.print_verbose("Multipier: ", pow(1.1, 2 - i))
        tools.print_verbose("Guessing length: ", round(len(bestGuess[2]) * pow(1.1, repeats-1 - i)))

        message = full_message[0:round(len(bestGuess[2]) * pow(1.1, repeats-1 - i))]
        tools.print_verbose(message)
        for map in maps:
            for locationKey in map.keys():
                if "location" in locationKey:
                    for cipherKey in map[locationKey].keys():
                        if "cipherText" in cipherKey and (stage == 0 or stage == int(cipherKey[10:])):
                            best.append([Levenshtein.ratio(map.get(locationKey).get(cipherKey), message),map.get(locationKey).get("plainText"), map.get(locationKey).get(cipherKey),  map.get(locationKey).get("mapUrl"), map.get("mapName"), cipherKey[10:]])
                            #if Levenshtein.ratio(map.get(locationKey).get(cipherKey), message) > 0.35:
                            #    print(map.get(locationKey).get("plainText") + " : " + str(Levenshtein.ratio(map.get(locationKey).get(cipherKey), message)));

        best.sort(key=lambda x: x[0])
        bestGuess = best[-1]

        if i == repeats-1:
            print(best[-1])
            print(best[-2])
            print(best[-3])

            print()

            bestGuess = best[-1]
            print("(🤖{certainty}%) (Stage {stage}) {plainText}: {map} | {url}".format(certainty = round(bestGuess[0]*100), plainText=bestGuess[1], map=bestGuess[4], url=bestGuess[3], stage=bestGuess[5]))
        else:
            tools.print_verbose(best[-1])
            tools.print_verbose(best[-2])
            tools.print_verbose(best[-3])

            tools.print_verbose()

            bestGuess = best[-1]
            tools.print_verbose("(🤖{certainty}%) (Stage {stage}) {plainText}: {map} | {url}".format(certainty = round(bestGuess[0]*100), plainText=bestGuess[1], map=bestGuess[4], url=bestGuess[3], stage=bestGuess[5]))

def beginning_better(message, stage):
    bestStart = 0
    bestEnd = len(message)
    bestRatio = calculate_ratio(message, stage);

    cutStartRatio = calculate_ratio(message[bestStart+1:bestEnd], stage);
    cutEndRatio = calculate_ratio(message[bestStart:bestEnd-1], stage);

    CONST_COUNTER = 3
    counter = CONST_COUNTER

    while (bestRatio <= cutEndRatio) or counter >= 0:
        print(counter)
        cutEndRatio = calculate_ratio(message[bestStart:bestEnd-1], stage);
        if bestRatio <= cutEndRatio:
            bestEnd -= 1
            bestRatio = cutEndRatio
            print("SHORTER RIGHT: ", message[bestStart:bestEnd])
            counter = CONST_COUNTER
        else:
            counter -= 1
            bestEnd -= 1

    print(message[bestStart:bestEnd])
    print(bestRatio, " vs ", cutStartRatio, " vs ", cutEndRatio)

    counter = -1 #CONST_COUNTER
    while (bestRatio <= cutStartRatio) or counter >= 0:
        print(counter)
        cutStartRatio = calculate_ratio(message[bestStart+1:bestEnd], stage);
        if bestRatio <= cutStartRatio:
            bestStart += 1
            bestRatio = cutStartRatio
            print("SHORTER LEFT: ", message[bestStart:bestEnd])
            counter = CONST_COUNTER
        else:
            counter -= 1


    print(message[bestStart:bestEnd])
    print(bestRatio, " vs ", cutStartRatio, " vs ", cutEndRatio)

def calculate_ratio(message, stage):
    import json
    import Levenshtein

    with open('beginning.json', 'r') as f:
        maps = json.load(f)

    best = []

    for map in maps:
        for locationKey in map.keys():
            if "location" in locationKey:
                for cipherKey in map[locationKey].keys():
                    if "cipherText" in cipherKey and (stage == 0 or stage == int(cipherKey[10:])):
                        best.append([Levenshtein.ratio(map.get(locationKey).get(cipherKey), message),map.get(locationKey).get("plainText"), map.get(locationKey).get(cipherKey),  map.get(locationKey).get("mapUrl"), map.get("mapName"), cipherKey[10:]])
                        #if Levenshtein.ratio(map.get(locationKey).get(cipherKey), message) > 0.35:
                        #    print(map.get(locationKey).get("plainText") + " : " + str(Levenshtein.ratio(map.get(locationKey).get(cipherKey), message)));

        best.sort(key=lambda x: x[0])
        return best[-1][0]
