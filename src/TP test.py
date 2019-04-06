# Calculates based on binary input

TP = 0
FP = 0
TN = 0
FN = 0

# Testing data
plist = [True, True, True, False, True, False, False, False, True, True, False, True, True]  # List of predicted values
rList = [True, True, False, False, True, True, False, False, False, False, True, True, True]  # Testing date

# Need to replace rList with user input from the web page based on Accept / Reject choices.

# Storing data into respective list based on result
trueP_L = []
falseP_L = []
trueN_L = []
falseN_L = []


def acc(TruePos, FalsePos, TrueNeg, FalseNeg):
    # Number of accurate results divided by the total data set.
    return (TrueNeg + TruePos) / (TruePos + FalsePos + TrueNeg + FalseNeg) * 100


if __name__ == '__main__':

    for x in range(len(plist)):
        # True positive: predicted = True and actual = True
        if plist[x] == rList[x] and rList[x] == True:
            TP += 1
            trueP_L.append(plist[x])  # Replace .append(list[x]) with the phrase data

        # False positive: predicted = True and actual = False
        if plist[x] is True and rList[x] != plist[x]:
            FP += 1
            falseP_L.append(plist[x])

        # True negative: predicted = False and actual = False
        if plist[x] is False and rList[x] == plist[x]:
            TN += 1
            trueN_L.append(plist[x])

        # False negative: predicted = False and actual = True
        if plist[x] != rList[x] and rList[x] is True:
            FN += 1
            falseN_L.append(plist[x])

    # Need to replace the outputted lists with the actual phrases
    print("True positive: ",   TP, trueP_L,
          "\nFalse positive:", FP, falseP_L,
          "\nTrue negative: ", TN, trueN_L,
          "\nFalse negative:", FN, falseN_L)

    print("\nAccuracy : %.2f%%" % acc(TP, FP, TN, FN))