import datetime,time
# Note: months may be positive, or negative, but must be an integer.   
# If favorEoM (favor End of Month) is true and input date is the last day of the month then  
# return an offset date that also falls on the last day of the month.  
def addmonths(date,months,favorEoM):   
    try:   
        targetdate = date  
        targetmonths = months+targetdate.month   
        if targetmonths%12 == 0:  
            # Month must be between 1 and 12 so a modulo remainder of 0 = 12  
            targetmonth = 12  
        else:  
            targetmonth = targetmonths%12  
        if favorEoM == True:  
            # Favor matching an End of Month date to an End of Month offset date.  
            testdate = date+datetime.timedelta(days=1)  
            if testdate.day == 1:  
                # input date was a last day of month and end of month is favored, so  
                # go to the FIRST of the month AFTER, then go back one day.  
                targetdate.replace(year=targetdate.year+int((targetmonths+1)/12),month=(targetmonth%12+1),day=1)  
                targetdate+=datetime.timedelta(days=-1)  
            else: 
                targetdate.replace(year=targetdate.year+int(targetmonths/12),month=(targetmonth))  
        else:  
            # Do not favor matching an End of Month date to the offset End of Month.  
            returndate = targetdate.replace(year=targetdate.year+int((targetmonths-1)/12),month=(targetmonth))  
        return returndate  
    except:  
        # There is an exception if the day of the month we're in does not exist in the target month  
        # Go to the FIRST of the month AFTER, then go back one day.  
        returndate = targetdate.replace(year=targetdate.year+int((targetmonths+1)/12),month=(targetmonth%12+1),day=1)  
        returndate+=datetime.timedelta(days=-1)   
        return returndate

def monthdelta(date, delta):
    m, y = (date.month+delta) % 12, date.year + ((date.month)+delta-1) // 12
    if not m: m = 12
    d = min(date.day, [31,
        29 if y%4==0 and not y%400==0 else 28,31,30,31,30,31,31,30,31,30,31][m-1])
    return date.replace(day=d,month=m, year=y)