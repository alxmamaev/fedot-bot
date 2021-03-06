import time

def add(bot, event_id, title, event_date, event_time):
    new_event = {"title":title, 
                "time": time.strptime(event_time,"%H:%M"),
                "id": event_id,
                "type": 0}

    shedule = bot.user_get(0, "shedule") or {}
    day_key = event_date

    day_shedule = shedule.get(day_key, [])
    for i, event in enumerate(day_shedule):
        event["time"] = time.strptime(event["time"], "%H:%M")
        day_shedule[i] = event

    day_shedule.append(new_event)
    day_shedule.sort(key = lambda x: x["time"])

    for i, event in enumerate(day_shedule):
        event["time"] = time.strftime("%H:%M", event["time"])
        day_shedule[i] = event


    shedule[day_key] = day_shedule
    shedule = bot.user_set(0, "shedule", shedule)

def delete(bot, event_id):
    shedule = bot.user_get(0, "shedule") or {}
    
    for day_key in shedule:
        day_shedule = shedule[day_key]
        for i, event in enumerate(day_shedule):
            if event_id == event["id"]:
                day_shedule.pop(i)
                shedule[day_key] = day_shedule
                break
        else: continue
        break

    bot.user_set(0, "shedule", shedule)

def get_day_shedule(bot, day_key):
    shedule = bot.user_get(0, "shedule") or {}
    day_shedule = shedule.get(day_key, [])

    return day_shedule

def get_shedule(bot):
    shedule = bot.user_get(0, "shedule") or {}
    shedule_list = []

    sorted_shedule = []
    for day in shedule:
        day_shedule = {"date":time.strptime(day, "%d.%m.%Y"), "events":[]}
        for event in shedule[day]:
            event["date"] = day + " " + event["time"]
            day_shedule["events"].append(event)

        sorted_shedule.append(day_shedule)       

    sorted_shedule.sort(key = lambda x: x["date"])

    shedule_list = []
    for day in sorted_shedule:
        shedule_list += day["events"]

    return shedule_list