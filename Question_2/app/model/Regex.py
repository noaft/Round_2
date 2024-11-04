import re
from datetime import datetime

def extract_recurrence(time_string):
    """
    Extract recurrence of week from string.
    Args:
        time_string (str): string contain hours.
    Return: 
        [List] : List of string recurrence detected.
    """
    pattern = r'\b(everytime|every time|any time|any day|everyday|every day|each day|every weekday|all week|every single day|daily)\b'
    match = re.findall(pattern, time_string.lower(), re.IGNORECASE)
    
    if match:
        return match
    else:
        return None

def extract_part_recurrence(time_string):
    """
    Extract recurrence of week from string.
    Args:
        time_string (str): string contain hours.
    Return: 
        [List] : List of string [art recurrence detected.
    """
    pattern = r'\b(everymorning|every morning|everyafternoon|every afternoon|everyevening|every evening|every night|everynight)\b'
    match = re.findall(pattern, time_string.lower(), re.IGNORECASE)
    
    if match:
        return match
    else:
        return None

def extract_day(time_string):
    """
    Extract  days of week from string.
    Args:
        time_string (str): string contain hours.
    Return: 
        [List] :List of string days of week detected.
    """

    pattern = r'\b(monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b'
    match = re.findall(pattern, time_string.lower(), re.IGNORECASE)
    
    if match:
        return match
    else:
        return None

def clean_time(time_string):
    """
    Clean string time extracted.
    Args:
        time_string (str): str contain time.
    Result:
        time (str): time add " " pre ['pm', 'am'] and clear space last string if have.
    """
    ar_ = []
    words = time_string.split()
    
    for word in words: 
        # Check if have 'am'or 'pm' in code
        if 'am' in word.lower() and word.lower() != 'am':
            number_part = word.lower().split('am')[0]
            ar_.append(number_part.strip())  # add to list
            ar_.append('am')  # add to list
        # Example: 3pm
        elif 'pm' in word.lower() and word.lower() != 'pm':
            number_part = word.lower().split('pm')[0]
            ar_.append(number_part.strip()) 
            ar_.append('pm')  
        # Remove last space in text if have
        elif word.strip(): 
            ar_.append(word)
    
    result = " ".join(ar_).strip()  # Kết hợp lại và loại bỏ khoảng trắng ở đầu và cuối

    return result


def get_start_end(time_string):
    """
    Get start and end time in string.
    Args:
        time_string (str): str contain time.
    Result:
        start_time: Start time in string.
        end_time: End time in string.
    """
    ar_ = clean_time(time_string).split(" ")

    # Example: 11 am to 12 am
    if ar_[1] in ['am', 'pm'] and len(ar_) == 5:
        start_time = ar_[0] + " " + ar_[1]
        end_time = ar_[3] + " " + ar_[4]
    # Example : 11 am to 12
    elif ar_[1] in ['am', 'pm']:
        start_time = ar_[0] + " " + ar_[1]
        end_time = ar_[3] + " " + ar_[1]
    # Example : 11 to 12 am
    else:
        start_time = ar_[0] + " " + ar_[3]
        end_time = ar_[2] + " " + ar_[3]
    
    return start_time, end_time


def extract_time(time_string):
    """
    Extract time from string.
    Args:
        time_string (str): string contain hours.
    Return: 
        Return string strt and end time detected.
    """
    
    # Regex to check valid time in 12-hour format
    pattern = r"((([1-9]|1[0-2])(:[0-5][0-9])?\s?(am|pm)?)\s?to\s(([1-9]|1[0-2])(:[0-5][0-9])?\s?(am|pm)?\s))"
    # add space for fit pattern
    time = time_string.split('.')[0]
    time += " "
    # Search for the time pattern in the string
    match = re.search(pattern, time.lower(), re.IGNORECASE)
    print(match.group(0))
    if match:
        return get_start_end(match.group(0))
    else:
        return None, None


def extract_one(message):
    """
    Extract availability and free time in text for each day of the week.
    Args:
        message (str): message from user
    Return:
        List[List[int]]: 2D list with day availability and free time in seconds
    """
    # Initialize a 2D array for the week (7 days)
    week_availability = [[0, []] for _ in range(7)]  # [availability (0 or 1), free time in seconds list]

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

    # Extract recurrence and part recurrence
    recurrence = extract_recurrence(message)
    part_recurrence = extract_part_recurrence(message)
    day_week = extract_day(message)

    # If recurrence detected, mark all days as available
    if recurrence:
        week_availability = [[1, []] for _ in range(7)]

    # For each day of the week, mark availability
    for day in day_week:
        if day in days_map:
            week_availability[days_map[day]][0] = 1  # Mark as available

    # Handle part recurrence to add free time in seconds
    if part_recurrence:
        for part in part_recurrence:
            # Morning
            if 'morning' in part:
                for i in range(7):
                    if week_availability[i][0] == 1:  # Check if available
                        week_availability[i][1].append((6 * 3600, 11 * 3600 + 59 * 60))  # 6 AM to 11:59 AM
            # Afternoon
            elif 'afternoon' in part:
                for i in range(7):
                    if week_availability[i][0] == 1:  # Check if available
                        week_availability[i][1].append((12 * 3600, 17 * 3600 + 59 * 60))  # 12 PM to 5:59 PM
            # Evening
            elif 'evening' in part:
                for i in range(7):
                    if week_availability[i][0] == 1:  # Check if available
                        week_availability[i][1].append((18 * 3600, 21 * 3600 + 59 * 60))  # 6 PM to 9:59 PM
            elif 'night' in part:
                for i in range(7):
                    if week_availability[i][0] == 1:  # Check if available
                        week_availability[i][1].append((18 * 3600, 21 * 3600 + 59 * 60))  # 6 PM to 9:59 PM

    if start_time:
        # Transform data
        start_time = caculate_time(start_time) 
        end_time = caculate_time(end_time)
    
        for i in range(7):
            if week_availability[i][0] == 1 and len(week_availability[i][1]) == 0:  # Check if available
                week_availability[i][1].append((start_time, end_time))
            elif week_availability[i][0] == 1 and check((start_time, end_time), week_availability[i][]) is False:

                

    return week_availability

def check(range_new, list_range):
    """
    Check if a new range is available in a list of existing ranges.
    
    Args:
        range_new (tuple): A tuple representing the new range (start, end).
        list_range (list): A list of tuples, each representing an existing range (start, end).
        
    Returns:
        bool: True if the new range is available, False if it overlaps with any existing range.
    """
    start_new, end_new = range_new
    
    for start_existing, end_existing in list_range:
        # Check for overlap
        if not (end_new <= start_existing or start_new >= end_existing):
            return False  # Overlap detected
    
    return True  # No overlap found

def caculate_time(start_time):
    """
    Transform str to int time
    Args:
        start_time (str): time needed tranform
    return:
        Time (int): time to tranform second
    """
    time = start_time.split(" ")[0]
    time = time.split(":")
    if len(time) == 2:
        time = int(time[0]) * 3600 + int(time[1]) * 60
    else len(time) == 3:
        time = int(time[0]) * 3600 + int(time[1]) * 60 + int(time[2])
    else:
        time = int(time[0]) * 3600
    
    if 'pm' in start_time:
        time += 12 * 3600
    
    return time

    
if __name__ == '__main__':
    # test for hours
    time_string = "every morning from 2 to 10:11 am."
    start_time, end_time = extract_time(time_string)
    print("Start time:", start_time, "\nEnd time:", end_time)
    # test for day
    time_string = "Monday and sunday from 2 to 10:11 am."
    day = extract_day(time_string)
    print(day)
    # test for day
    time_string = "everytime from 2  to 10:11 am."
    recurrence = extract_recurrence(time_string)
    print(recurrence)
    # test for day
    time_string = "everymorning and every night from 2  to 10:11 am."
    recurrence = extract_part_recurrence(time_string)
    print(recurrence)
