from datetime import datetime, timedelta
# https://stackoverflow.com/questions/441147/how-to-subtract-a-day-from-a-date
d = datetime.today() - timedelta(days=days_to_subtract)
print (d)

# https://www.codegrepper.com/code-examples/python/how+to+get+day+before+python+date
yesterday = datetime.today() - timedelta(days = 1, hours = 5 )


# # https://stackoverflow.com/questions/64167141/how-do-i-schedule-a-function-to-run-everyday-at-a-specific-time-in-discord-py
# def seconds_until(hours, minutes):
#     given_time = datetime.time(hours, minutes)
#     now = datetime.datetime.now()
#     future_exec = datetime.datetime.combine(now, given_time)
#     if (future_exec - now).days < 0:  # If we are past the execution, it will take place tomorrow
#         future_exec = datetime.datetime.combine(now + datetime.timedelta(days=1), given_time) # days always >= 0
#     return (future_exec - now).total_seconds()
    

# async def my_job_forever(self):
#     while True:  # Or change to self.is_running or some variable to control the task
#         await asyncio.sleep(seconds_until(11,58))  # Will stay here until your clock says 11:58
#         # put code here to check if its monday
#         # put code here to check if its tuseday
#         #  etc
#         print("See you in 24 hours from exactly now")
#         await asyncio.sleep(60)  # Practical solution to ensure that the print isn't spammed as long as it is 11:58

# async def my_job_forever_2(self):
#     while True:  # Or change to self.is_running or some variable to control the task
#         await asyncio.sleep(seconds_until(11,58))  # Will stay here until your clock says 11:58
#         # put code here to check if its tuseday at 2:31
#         # put code here to check if its wednesday
#         #  etc
#         print("See you in 24 hours from exactly now")
#         await asyncio.sleep(60)  # Practical solution to ensure that the print isn't spammed as long as it is 11:58



# https://www.reddit.com/r/Discord_Bots/comments/sr452y/discord_py_execute_command_on_a_specific_weekday/
@tasks.loop(minutes=60.0)
    async def mondayjob():
    # 0 = monday, 1 = tuesday...
    weekday = datetime.datetime.weekday(datetime.datetime.now())
    if weekday == 0:
        await asyncio.sleep(seconds_until(12, 00))
        [Do your stuff]

# Calculates the time in seconds until hh:mm is reached
def seconds_until(hours, minutes):
    given_time = datetime.time(hours, minutes)
    now = datetime.datetime.now()
    future_exec = datetime.datetime.combine(now, given_time)
    if (future_exec - now).days < 0: # If we are past the execution, it will take place tomorrow
        future_exec = datetime.datetime.combine(now + datetime.timedelta(days=1), given_time) # days always >= 0
    return (future_exec - now).total_seconds()