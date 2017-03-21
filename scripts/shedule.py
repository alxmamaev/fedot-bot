import redis
import json 
import time
import os

rds = redis.from_url(os.environ.get("REDIS_URL","redis://localhost:6379"))

key = "user:0:shedule"

shedule = rds.get(key)
if type(shedule) is bytes: shedule = shedule.decode('utf-8')
if shedule: shedule = json.loads(shedule)
shedule = shedule or {}


cur_date = time.strftime("%d.%m.%Y")
cur_time = time.localtime()

flag = False
for i, event in enumerate(shedule[cur_date]):
	event_time = time.strptime(event["time"], "%H:%M")
	if event_time.tm_hour <= cur_time.tm_hour and event_time.tm_min <= cur_time.tm_min: 
		if not flag: shedule[cur_date][i]["type"] = 1
		else: shedule[cur_date][i]["type"] = 2
		flag = True
	else: shedule[cur_date][i]["type"] = 0

shedule = json.dumps(shedule)
rds.set(key, shedule)

