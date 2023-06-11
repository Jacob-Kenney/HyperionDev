import math

#Function to retrive the users decision on which calculation to make, taking no input
def calculation_type():
    #Assign a temporary variable, decision, to the users decision
    decision = input('Please enter:\n1 - For investment,\n2 - For mortgage,\nDecision: ')
    #If the decision variable is investment
    if decision == '1':
        #Call investment function
        investment()
    #Else if decision is mortgage
    elif decision == '2':
        #Call mortgage function
        mortgage()
    #Else
    else:
        #Recursive call to current function
        calculation_type()

#Function to get calculation parameters (deposit, interest rate, period, type of investment), taking borrow or invest as input
def parameter_getter(decision):
    #if investing
    if decision == 'i':
        #Assign a temporary variable, deposit, to the inputted principal amount
        deposit = int(input('Please enter the initial deposit: '))
        #Assign a temporary variable, interest, to the interest rate (as an integer)
        interest = int(input('Please enter the annual expected return percentage, (1 == 1%): '))
        #Assign a temporary variable, years, to the duration of the investment (in years)
        years = int(input('Please enter the number of years you plan to invest: '))
        #Assign a temporary variable, type, to the type of interest accrued (compound or simple)
        interest_type = str(input('Please enter the type of interest (simple or compound)'))
        #if type is simple or comound
        if interest_type.lower() == 'simple' or 'compound':
            #return deposit, interest, years, type
            return deposit, interest, years, interest_type
        #else
        else:
            #Recursive call to current function
            parameter_getter(decision)
    #if borrowing
    if decision == 'b':
        #Assign a temporary variable, value, to the inputted home value
        value = int(input('Please enter the home value: '))
        #Assign a temporary variable, interest, to the annual rate (as an integer)
        interest = int(input('Please enter the annual interest rate, (1 == 1%): '))
        #Assign a temporary variable, years, to the duration of the investment (in years)
        years = int(input('Please enter the number of years you will have this mortgage: '))
        #return value, interest, years
        return value, interest, years

#Function to calculate the interest on an investment, taking no input
def investment():
    #Assign temporary variables, deposit, interest, years, type to the result of a call to parameter getter
    deposit, interest, years, interest_type = parameter_getter('i')
    #If interest is simple
    if interest_type == 'simple':
        #print (deposit x (1 + (interest x years))) (the expected value upon redemption)
        print(str(deposit * (1 + ((interest / 100) * years ))))
        #call the user decision function for another calculation
        calculation_type()
    #Elif interest is compound
    elif interest_type == 'compound':
        #assign a temporary variable, result, to (deposit x ((1 + interest) ^ years)) (the expected value upon redemption)
        result = (deposit * ((1 + (interest / 100)) ** years))
        result = round(result, 2)
        #print result
        print('The amount your investment will be worth at the end of the period is: £'+str(result))
        #call the user decision function for another calculation
        calculation_type()


#Function to calculate the interest on bonds
def mortgage():
    #Assign temporary variables, value, interest, years to the result of a call to parameter getter
    value, interest, years = parameter_getter('b')
    #Set interest to (interest / 12)
    interest = (interest / 100) / 12
    #Set duration to (years x 12)
    duration = years * 12
    #assign a temporary variable, result, to (interest * value)
    result = (interest * value)
    #assign a temporary variable, denominator, to (1 - (1 + interest) ^ (- duration))
    denominator = (1 - (1 + interest) ** (-duration))
    #set result to result / denominator
    result = (result / denominator)
    result = round(result, 2)
    #print result
    print('The amount you must repay each month is: £'+str(result))
    #call the user decision function for another calculation
    calculation_type()


#Call user decision function
calculation_type()
