from datetime import datetime, timedelta
# https://stackoverflow.com/questions/441147/how-to-subtract-a-day-from-a-date
d = datetime.today() - timedelta(days=days_to_subtract)
print (d)