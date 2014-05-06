#---------------------------------------------
# form validation methods
# --------------------------------------------

def preprocess_new_pitch(data):
    ''' preprocess a new pitch creation '''

    amount1 = ""
    amount2 = ""

    for element in data['amount-1']:
        if element.isdigit():
            amount1 += element

    for element in data['amount-2']:
        if element.isdigit():
            amount2 += element

    return amount1,amount2


