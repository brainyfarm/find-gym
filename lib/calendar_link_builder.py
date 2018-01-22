def get_google_calendar_time(time_string):
  from datetime import *
  split_time_list = time_string.split(' ')
  split_date_list = split_time_list[0].split('-')
  combined_date_string = ''.join(split_date_list[::-1])
  joined_time_string = ' '.join([i for i in split_time_list if split_time_list.index(i) != 0])
  joined_time_24hr = str(datetime.strptime(joined_time_string, '%I:%M %p')).split(' ')[1]
  google_calendar_dt_format = combined_date_string + 'T' + joined_time_24hr.replace(':','')
  return google_calendar_dt_format + '/' + google_calendar_dt_format  

def build_link(booking_details):
    event_name = booking_details['gym'] + ': ' + 'Session Booking'
    booking_link = 'http://localhost:5000/session/confirm/' + str(booking_details['id_string'])
    calendar_link = 'https://www.google.com/calendar/render?action=TEMPLATE&text='+ event_name + '&dates=' + get_google_calendar_time(booking_details['date_time']) + '&details=' + 'For+details,+link+here:+' + booking_link + '&location=' + booking_details['address'] + '&sf=true&output=xml'
    return calendar_link
