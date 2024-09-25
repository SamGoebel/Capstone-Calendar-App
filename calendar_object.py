import calendar 
import time


class CalendarCreation():
    
    def DateObject(self, day, month, year):
       
        weekday = calendar.day_name[calendar.weekday(year, month, day)]
         # Format the date as: Weekday, Month Day, Year
        date_str = f"{weekday}, {calendar.month_name[month]} {day}, {year}"
        print(date_str, "\n")
        
        #return (cal_str)

    def CalendarPrint(self, month, year):
        
        cal = calendar.TextCalendar(calendar.SUNDAY)
        cal_str = cal.formatmonth(year, month)

        # Print the calendar
        print(cal_str)
       
'''
yy = 2017
mm = 11
print(calendar.month(yy, mm)) 
'''