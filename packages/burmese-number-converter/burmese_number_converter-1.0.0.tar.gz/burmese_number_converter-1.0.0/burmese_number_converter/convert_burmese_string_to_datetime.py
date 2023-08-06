BURMESE_NUMBERS = {
    1: '၁', 2: '၂', 3: '၃', 4: '၄', 5: '၅',
    6: '၆', 7: '၇', 8: '၈', 9: '၉', 0: '၀'
}


def convert_burmese_date_time(datetime_obj, str_format_time):
    date_time_to_string = list(datetime_obj.strftime(str_format_time))
    for date_time in date_time_to_string:
        date_time_to_string[date_time_to_string.index(date_time)] = BURMESE_NUMBERS[
            int(date_time)] if date_time.isdigit() else date_time
    return ''.join(date_time_to_string)


