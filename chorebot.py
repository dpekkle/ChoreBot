import praw
import pickle
import os
from datetime import datetime
import time
import sys

folder = "..." 				# e.g C://Users/Public/ChoreBot/
bot_username = "..." 		# username of the bot you wish to send messages from
bot_password = "..." 		# password of the bot
target_username = "..." 	# the reddit username of the account you wish to receive messages


def msgDish():
	r = praw.Reddit(user_agent ='Chore Bot')
	r.login(bot_username, bot_password, disable_warning=True)
	r.send_message(target_username, 'Time to do some house work', 'Time to do the dishes. \n\n Collect any dishes you can find around the house, bring them to the kitchen, then clean up as much as you can.')
	print ("Sent dishes message")
	return
	
def msgLaundry():
	r = praw.Reddit(user_agent ='Chore Bot')
	r.login(bot_username, bot_password, disable_warning=True)
	r.send_message(target_username, 'Time to do some house work', 'You should do some laundry. \n\n Put anything in the laundry room in the washer and hang them up'')
	print ("Sent laundry message")
	return

print ("________________________________________________________________\n")

if not os.path.exists(folder + "store2.pckl"):
	print ("New pickle stored")
	list_of_datetimes = [datetime.now(), datetime.now()]
	f = open(folder + '/store2.pckl', 'wb')
	pickle.dump(list_of_datetimes, f)
	f.close()
	msgLaundry()			
	msgDish()	
	
log = open(folder + 'log.txt', 'a')	
log.write("\n\n~~~~~~~~NEW RUN ~~~~~~~~~~~~ \n\n")			
log.close()
	
count = 0;
while True:
	count += 1
	currenttime = datetime.now()
	if os.path.exists(folder + "store2.pckl"):
		f = open(folder + 'store2.pckl', 'rb')
		list_of_oldtimes = pickle.load(f)
		f.close()
		
		laundryDelta = ((currenttime-list_of_oldtimes[0]).total_seconds())
		dishDelta = ((currenttime-list_of_oldtimes[1]).total_seconds())
		
		#logs and output
		log = open(folder + 'log.txt', 'a')	
		log.write("Time: " + currenttime.strftime('%H:%M:%S %a %d/%m/%Y') + "\t|\tLast Laundry: " + list_of_oldtimes[0].strftime('%H:%M:%S %a %d/%m/%Y') + "\n")			
		log.close()
		sys.stdout.write(str(count) + "\t|\tLaundry: " + str(round(((7 * 86400) - laundryDelta)/60, 0)) + " min")
		sys.stdout.write("\t|\tDishes: " + str(round(((3 * 86400) - dishDelta)/60, 0)) + " min\n")

		if ((currenttime-list_of_oldtimes[0]).days >= 7):
			msgLaundry()			
			list_of_oldtimes[0] = currenttime;
			f = open(folder + 'store2.pckl', 'wb')
			pickle.dump(list_of_oldtimes, f)
			f.close()
			
		if ((currenttime-list_of_oldtimes[1]).days >= 3):	
			msgDish()
			list_of_oldtimes[1] = currenttime;
			f = open(folder + 'store2.pckl', 'wb')
			pickle.dump(list_of_oldtimes, f)
			f.close()
	else:
		sys.stdout.write("ERROR: Storage file doesn't exit!")
	time.sleep(120)






