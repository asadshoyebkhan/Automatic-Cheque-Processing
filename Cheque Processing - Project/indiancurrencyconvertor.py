def num2words(num):
    under_20 = ['zero','one','two','three','four','five','six','seven','eight','nine','ten','eleven','twelve','thirteen','fourteen','fifteen','sixteen','seventeen','eighteen','nineteen']
    tens = ['twenty','thirty','forty','fifty','sixty','seventy','eighty','ninety']
    above_100 = {100: 'hundred',1000:'thousand', 100000:'lakhs', 10000000:'crores', 1000000000:'arab'}

    if num < 20:
         return under_20[num]

    if num < 100:
        return tens[(int)(num/10)-2] + ('' if num%10==0 else ' ' + under_20[num%10])

    # find the appropriate pivot - 'Million' in 3,603,550, or 'Thousand' in 603,550
    pivot = max([key for key in above_100.keys() if key <= num])

    return num2words((int)(num/pivot)) + ' ' + above_100[pivot] + ('' if num%pivot==0 else ' ' + num2words(num%pivot))

