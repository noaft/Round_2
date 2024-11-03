import re
from datetime import datetime

def extract_time(time_string):
    pass

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
        # Kiểm tra nếu từ có chứa "am" hoặc "pm"
        if 'am' in word.lower() and word.lower() != 'am':
            # Tách phần số và thêm "am"
            number_part = word.lower().split('am')[0]
            ar_.append(number_part.strip())  # Thêm số đã tách
            ar_.append('am')  # Thêm 'am'
        elif 'pm' in word.lower() and word.lower() != 'pm':
            # Tách phần số và thêm "pm"
            number_part = word.lower().split('pm')[0]
            ar_.append(number_part.strip())  # Thêm số đã tách
            ar_.append('pm')  # Thêm 'pm'
        elif word.strip():  # Nếu từ không phải là khoảng trắng
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
        Return hour detected.
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

if __name__ == '__main__':
    #test
    time_string = "every morning from 2  to 10:11 am."
    start_time, end_time = extract_time(time_string)
    print("Start time:", start_time, "\nEnd time:", end_time)
