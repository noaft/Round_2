from Regex import extract_recurrence, extract_part_recurrence, extract_day, extract_time
from datetime import datetime
from QA_model import QA_model as model

def detect_time(start_time, end_time, recurrence, day_week, part_recurrence):
    """
    Extract all time and format it.
    Args:
        start_time (str): start time in text
        end_time (str): end time in text
        recurrence (str): recurrence in text
        day_week (str): each weekday mentioned in the text
    Returns:
        List: A list binary where each inner list represents a day.
        If a day has availability, the first element is 1, and the second element is a list of time ranges.
    """

    Time= [[0,[]] for _ in range(7)]

    map_ = {
        'morning': (6 * 60, 11 * 60 + 59),      # 6:00 AM to 11:59 AM
        'afternoon': (12 * 60, 17 * 60 + 59),    # 12:00 PM to 5:59 PM
        'evening': (18 * 60, 20 * 60 + 59),      # 6:00 PM to 8:59 PM
        'night': (21 * 60, 23 * 60 + 59)         # 9:00 PM to 11:59 PM
    }

    # Map days of the week to indices
    days_map = {
        'monday': 0,
        'tuesday': 1,
        'wednesday': 2,
        'thursday': 3,
        'friday': 4,
        'saturday': 5,
        'sunday': 6
    }

    # If recurrence is true, mark all days as available
    if recurrence or part_recurrence:
        for i in range(7):
            Time[i][0] = 1
    else:
        # If specific days are mentioned, mark only those as available
        for day in day_week:
            if day in days_map:
                Time[days_map[day]][0] = 1
    
    # Add specific start and end times if provided
    if start_time:
        st = time_to_seconds(start_time)
        et = time_to_seconds(end_time)
        for i in range(7):
            if Time[i][0] == 1:
                Time[i][1].append((st, et))

    # Add predefined time ranges based on part recurrence (morning, afternoon, etc.)
    if part_recurrence:
        for part in map_.keys():
            if part in part_recurrence:    
                for i in range(7):
                    if Time[i][0] == 1:
                        Time[i][1].append(map_[part])

    if start_time is None:
        for i in range(7):
            if Time[i][0] == 1:
                Time[i][1].append((0, 1440))

    return Time

def subtract_intervals(free, busy):
    """
    Subtracts intervals from a list of available (free) intervals using a list of unavailable (not_free) intervals.
    Args:
        free (list of tuples): A list of available time.
        not_free (list of tuples): A list of unvaiable time.

    Returns:
        list of binary: A list of non-overlapping intervals from the `free` list after subtracting intervals from 
                        the `not_free` list.
    """

    all_frees = [0 for _ in range(10080)]

    for i in range(10080):
        all_frees[i] = free[i] - busy[i]
    return all_frees

def time_to_seconds(time_str):
    """
    Convert a time string in the format 'hh:mm:ss AM/PM' or 'hh:mm AM/PM' to seconds.
    
    Args:
        time_str (str): The time string to convert.
        
    Returns:
        int: The time in seconds from midnight.
    """
    try:
        # Parse the time string to a datetime object
        len_ = len(time_str.split(":"))
        if len_ == 3:
            time_obj = datetime.strptime(time_str.strip(), '%I:%M:%S %p')  # Format with seconds
        elif len_ == 2:
            time_obj = datetime.strptime(time_str.strip(), '%I:%M %p')  # Format without seconds
        else:
            time_obj = datetime.strptime(time_str.strip(), '%I %p')  # Format without seconds    
        # Convert hours, minutes, and seconds to seconds
        seconds = time_obj.hour * 60 + time_obj.minute
        return seconds
    except ValueError:
        print("Invalid time format. Please use 'hh:mm:ss AM/PM' or 'hh:mm AM/PM'.")
        return None

def extract_one(message, model, full_text):
    """
    Extract availability and free time in text for each day of the week.
    Args:
        message (str): message from user
    Return:
        List[List[int]]: 2D list with day availability and free time in seconds
    """
    # Map days of the week to indices
    
    avaiable_time = [[0,[]] for _ in range(7)]
    avaiable_time_fake = []
    days_map = {
        'monday': 0,
        'tuesday': 1,
        'wednesday': 2,
        'thursday': 3,
        'friday': 4,
        'saturday': 5,
        'sunday': 6
    }
    
    # Extract recurrence and part recurrence
    # recurrence = extract_recurrence(message)
    part_recurrence = extract_part_recurrence(message)
    # day_week = extract_day(message)
    list_time, full_time = extract_time(message)
    if list_time != [None , None]:
        for i in range(len(list_time)):
            start_time = list_time[i][0]
            end_time = list_time[i][1]
            day_week = extract_day(model.get_day(full_text, full_time[i]))
            if day_week:
                recurrence = extract_recurrence(message)
                avaiable_time_fake.append(detect_time(start_time, end_time, recurrence, day_week, part_recurrence))
            else:
                recurrence = extract_recurrence(message)
                avaiable_time_fake.append(detect_time(start_time, end_time, recurrence, None, part_recurrence))
    else:
        recurrence = extract_recurrence(message)
        day_week = extract_day(message)
        avaiable_time_fake.append(detect_time(None, None, recurrence, day_week, part_recurrence))

    for avaiables in avaiable_time_fake:
        for i in range(7):
            if avaiables[i][0] == 1:
                for j in avaiables[i][1]:
                    avaiable_time[i][0] = 1
                    avaiable_time[i][1].append(j)                   
    
    return transform_binary(avaiable_time)

def detect_avaiable(free, busy, model, context):
    """
    Get free time onion busy time:
    Args:
        free (List[[]]): free time.
        busy (List[[]]): busy time.
        model (class): model Nlp
        context (str): context
    Return:
        List of free time in test
    """
    if free and busy is None:
        return extract_one(free, model, context)
    elif free and busy:
        free_avaiable = extract_one(free, model, context)
        busy_time = extract_one(busy, model, context)
        result = subtract_intervals(free_avaiable, busy_time)
        return result

    free_avaiable = [[1,[(0, 10080)]] for _ in range(7) ]
    result = subtract_intervals(free_avaiable, busy_time)
    return result

def transform_binary(Time):
    """
    Transform all list to array binary.
    Args:
        time (List[[]]): list time avaiable
    Return:
        Return (List): [0,1,1,...] binary array
    """
    List = [0 for _ in range(10080)]
    for i in range(7):
        if Time[i][0] == 1:
            for (start, end) in Time[i][1]:
                for j in range(start + i * 1440, end + i * 1440):
                    List[j] = 1
    print(List)
    return List


def conflict_solution(*arg):
    """
    Detect and solotion conflict
    Args:
        arg: all of list time
    return:
        return all time not conflict and number can join
    """
    result = arg[0]
    for i in range(1, len(arg)):
        for j in range(10080):
            result[j] +=  arg[i][j]
    return result

if __name__ == '__main__':
    model_name = "deepset/xlm-roberta-large-squad2"
    model = model(model_name, model_name)
    context1 = "I'm avaiable every morning, except on Wednesday from 9 to 10 AM."
    context2 = "I'm avaiable every morning, except on Tuesday from"
    free, busy = model.get_time(context1)
    r = detect_avaiable(free, busy, model, context1)
    print(r)
    # context = "i am avaiable Monday every time and Tuesday 1 to 10 pm."