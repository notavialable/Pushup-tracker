from datetime import datetime
from colorzero import Color
from statistics import stdev
from data_2025 import *


todays_reps = 80
rest = False

if to_copy := False:	
	print(*[f'{d:0=3}: {int(n):0=3} → {"|"*round(n/5)}\n' for d, n in enumerate(reps, 1)], sep='')
	exit()
	
def relative_perc(num, data):
	return round(num * 100 / sum(data), 2)
	
def get_statistics(data):
	total, len_ = sum(data), len(data)
	media = total / len_
	deviation = stdev(data)
	
	max_ = max(data)	
	day_of_max = data.index(max_) + 1
	
	rest_days = data.count(0)
	rest_days_perc = 100 * rest_days / len_

	return total, len_, max_, day_of_max, media, deviation, rest_days, rest_days_perc,


def day_amount(day: int):
	return sum(reps[day::7])
	
def get_graphic(progress):
	graph_length = 40
	bars = '|' * round(graph_length * progress)
	
	print( '   | ╓', '─'*35, '╖') 
	print(f'   |  ⟨ {bars:<40} ⟩')
	print( '   | ╙', '─'*35, '╜') 


def print_bars(flag, skip_info=False):
	global past_week_info, this_week_info, content
	
	graphs_bar = '|' * bars_amount
	isRestDay = reps[day] is rest
	bar_content = '\t—[ Rest Day ]—' if isRestDay else graphs_bar	
	
	if show_weeks:
		#star = f'{Color("yellow")}★ {brightness[lvl]}'
		star = f'{Color("darkorange")}★ {Color("lightgray")}'
		#star = '★'
		
		pre_info = f'|+{"—" * 5} {star * perfect_week:^3}'
		
		weekday = list(weekdays_amount)[day%7]
		initial = weekday[0]
	
	
	match flag:
		case 'content':
			print(f'|{day+1:3}'*(not skip_info), end='')
			
			if show_weeks:
				print(f' ⟨{initial}⟩ ', end='')
			
			print(f'→ {bar_content}')
			
		case 'past_week_info':
			print(pre_info, f'Week {week+week_offset}: {weeks_total} [{weeks_media}]')
			
		case 'this_week_info':
			print(pre_info, f'Current Week: {this_week_total} [{this_week_media}]')
			
		case 'today':
			print(f'|╙ ╖  ~ TODAY ~')
			
			if show_weeks:
				print(f'   | Day: {len_} ({weekday})')
			
			print(f'   | Reps: {int(reps[-1])} out of {todays_reps} ({100*todays_progress:.0f}%)')
			get_graphic(todays_progress)
	return


print(f'{Color("lightgray")}')

total, len_, max_, day_of_max, media, deviation, rest_days, rest_days_perc = get_statistics(reps)
weekdays_amount = {
	'Monday':    0,
	'Tuesday':   0,
	'Wednesday': 0,
	'Thursday':  0,
	'Friday':    0,
	'Saturday':  0,
	'Sunday':    0,
}


show_weeks = True

# 50 is how many bars fit in one line. There will only fit 45 if the day of the week is shown.
length_ratio = (45 if show_weeks else 50) / max_

total_perfect_weeks = []
maxStreak = streak = 0
total_bars = 0

for day, n in enumerate(reps):
	
	if day+1 == len_:
		
		todays_progress = (reps[-1] / todays_reps)
		print_bars('today')
		
		continue
		
	bars_amount = round(n*length_ratio)
	total_bars += bars_amount
	
	# Every 7 days it prints the week info 
	if show_weeks and day % 7 == 0:
		week = (day // 7) + 1
		
		# Given a day this line calculates the reps within the next 7 days and the media
		week_amounts = reps[day : day+7]
		weeks_total = sum(week_amounts)
		weeks_media = weeks_total // 7
		
		# If all the days of the week have the same amount of reps, it is a perfect week
		perfect_week = week_amounts.count(week_amounts[0]) == len(week_amounts) and week_amounts[0]
		if perfect_week:
			total_perfect_weeks.append(week)
			
		# This calculates the remaining days, if they are less than a full week, calculates the total amount of reps in that period of days.
		if (this_week_days := len_ - day) < 7: 
			this_weeks_reps = reps[-this_week_days:]
			this_week_total = sum(this_weeks_reps)
			this_week_media = this_week_total // this_week_days
			
			this_week_info = f'Current Week: {this_week_total}'
			print_bars('this_week_info')

		else:
			print_bars('past_week_info')
		
	print_bars('content')
	
	# This mess just works.
	maxStreak, streak = (max(streak, maxStreak), 0) if (n == 0 and n is not rest) else (maxStreak, streak + (0 if n is rest else 1))
	
	
# This line is to count as a max streak the ongoing streak
maxStreak = max(streak, maxStreak)
is_active_streak = streak == maxStreak

separator = ('≈•'*26)[:-1]

print('\n\n' + separator + '')

print('   Total    Media     Deviation    Days inactive')
print(f'{total:7}{media:10,.2f}{deviation:12,.3f}{rest_days:9} ~ {rest_days_perc:.2f}%')
print(f' » Max at day {day_of_max} with {max_} reps.')


if is_active_streak:
	streak_info = f' » Current streak is  {streak:3} days.'
	
else:
	streak_info = f' » Best streak lasted {maxStreak:3} days.'

print(streak_info)

if streak:
	streaks_media = sum(reps[-streak:]) / streak
	print(f' » Media in this streak: {streaks_media:.2f}.')

if show_weeks:
	print(f' » Amount of perfect weeks: {len(total_perfect_weeks):2}.')

if show_bar_value := False:
	print(f'\n{Color("gray")} 1 bar = {total / total_bars :.2f} | {max_/40 :.2f} reps{Color("white")}')


year_progress = 100 * (1 - (len_ + 8) / 365)
print(f'\nRemaining time: {year_progress:.1f}%')

reps_progress = 100 * (1 - total / goal)
print(f'Remaining reps: {reps_progress:.1f}%')	


print('\n\n' + separator + '\n')

for n, day in enumerate(weekdays_amount):
	weekdays_amount[day] = day_amount(n)
	n_perc = relative_perc(weekdays_amount[day], reps)
	
	bar_amount = round(9*weekdays_amount[day]*length_ratio/max(1,(len_//7))) - 72
	#bar_amount = round(weekdays_amount[day]*length_ratio/(len_//7))
	
	val = weekdays_amount[day]
	print(f' {day[:1]:<1}» {val:<3}› {n_perc:.1f}% {"|" * bar_amount}')
print(f'{Color("gray")} {" "*35} [Not to scale]')

if show_goal := True:
	days = datetime.now().timetuple().tm_yday
	length_year = 365

	dailyRepsGoal = round((goal - total) / (length_year - days))
	
	print(f'\n{Color("gray")} you need to do {dailyRepsGoal} reps everyday to reach {goal} by the end of the year.{Color("black")}')