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
        List[[(1|0), ()], [], [], [], [], [], []]: A list where each inner list represents a day.
        If a day has availability, the first element is 1, and the second element is a list of time ranges.
    """

    Time= [[0,[]] for _ in range(7)]

    map_ = {
        'morning': (6 * 3600, 11 * 3600 + 59 * 60 + 59),      # 6:00 AM to 11:59:59 AM
        'afternoon': (12 * 3600, 17 * 3600 + 59 * 60 + 59),    # 12:00 PM to 5:59:59 PM
        'evening': (18 * 3600, 20 * 3600 + 59 * 60 + 59),      # 6:00 PM to 8:59:59 PM
        'night': (21 * 3600, 23 * 3600 + 59 * 60 + 59)         # 9:00 PM to 11:59:59 PM
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
    if recurrence:
        for i in range(7):
            Time[i][0] = 1
    else:
        # If specific days are mentioned, mark only those as available
        for day in day_week:
            if day in days_map:
                print(days_map[day])
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

    return Time

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
        seconds = time_obj.hour * 3600 + time_obj.minute * 60 + time_obj.second
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
    print(len(list_time))
    if len(list_time) != 0:
        for i in range(len(list_time)):
            start_time = list_time[i][0]
            end_time = list_time[i][1]
            day_week = extract_day(model.get_day(full_text, full_time[i]))
            recurrence = extract_recurrence(message)
            avaiable_time_fake.append(detect_time(start_time, end_time, recurrence, day_week, part_recurrence))
    
    for avaiables in avaiable_time_fake:
        for i in range(7):
            if avaiables[i][0] == 1:
                for j in avaiables[i][1]:
                    avaiable_time[i][0] = 1
                    avaiable_time[i][1].append(j)                   

    return avaiable_time

if __name__ == '__main__':
    model_name = "deepset/xlm-roberta-large-squad2"
    model = model(model_name, model_name)
    context = "i am avaiable Monday 2 to 10:11 am and Tuesday 1 to 10 pm."
    free, busy = model.get_time(context)
    print(extract_one(free, model, context))
    # context = "i am avaiable Monday every time and Tuesday 1 to 10 pm."
    # free, busy = model.get_time(context)
    # print(extract_one(free, model, context))