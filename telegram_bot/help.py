from datetime import datetime

def get_today(statuses):
  today = datetime.now().date().isoformat()
  today_status = None
  for status in statuses:
    if status['date'] == today:
      today_status = status
      break
  return today_status
  
def get_today_status(today_status):
  if not today_status: 
    return "❌"
  if today_status['is_completed'] == False:
    return "❌"
  return "✅"


