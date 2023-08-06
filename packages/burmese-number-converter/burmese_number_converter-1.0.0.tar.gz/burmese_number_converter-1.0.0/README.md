# Burmese Number Converter

### about

    author : Han Zaw Nyein
    email  : hanzawnyineonline@gmail.com

### Date, Datetime

```python
import datetime
from burmese_number_converter import convert_burmese_date_time, BURMESE_NUMBERS

if __name__ == '__main__':
    print(BURMESE_NUMBERS[0], BURMESE_NUMBERS[1], BURMESE_NUMBERS[2], BURMESE_NUMBERS[3])

    current_date_time = datetime.datetime.today()
    converted_date_time_string = convert_burmese_date_time(datetime_obj=current_date_time, str_format_time="%m/%d/%Y, %H:%M:%S")
    print(converted_date_time_string)

    converted_date_string = convert_burmese_date_time(datetime_obj=current_date_time, str_format_time="%m/%d/%Y")
    print(converted_date_string)

    current_date = datetime.date.today()
    converted_date_obj_input_string = convert_burmese_date_time(datetime_obj=current_date, str_format_time="%m/%d/%Y")
    print(converted_date_obj_input_string)

```

```text
# output
၀ ၁ ၂ ၃
၁၁/၀၄/၂၀၂၂, ၂၃:၄၁:၁၇
၁၁/၀၄/၂၀၂၂
၁၁/၀၄/၂၀၂၂
```