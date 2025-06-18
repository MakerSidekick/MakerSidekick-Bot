min_meter = 0
max_meter = 100
happy_add = 5
sad_subtract = 10
"""
+ -> Increase Happiness
- -> Increase Dissatisfaction/Distrust
current_value -> Current Happiness Meter Value
ext_multiplier -> In case we want to change the multiplier externally
"""
def meter(state="add", current_value=35, ext_multiplier=1):
    # Our Change, after multipliers and all
    delta = 0
    result = 0

    # handle incorrect values
    if state != "add" and state != "reduce":
        print("Error!")
        return current_value

    if current_value >= max_meter and state == "add":
        print("Current Value already at Maximum!")
        return max_meter # Value above maximum, return 100
    elif current_value <= min_meter and state == "reduce":
        print("Current Value already at Minimum!")
        return min_meter # Value below minimum, return 0

    if state == "add":
        if current_value < 35:
            delta = (happy_add * ext_multiplier * 1.35) # Bot is sad, we need to make it happier faster
        else:
            delta = (happy_add * ext_multiplier)
        result = current_value + delta
    elif state == "reduce":
        if current_value > 75:
            delta = (sad_subtract * ext_multiplier * 0.5) # Bot knows owner is a good hooman, this must be a mistake
        else:
            delta = (sad_subtract * ext_multiplier)
        result = current_value - delta

    print(f"Happiness {state} by {delta}! Current Value: ", result)
    
    if result >= max_meter:
        return max_meter # Value above maximum, return 100
    elif result <= min_meter:
        return min_meter # Value below minimum, return 0
    else:
        return result