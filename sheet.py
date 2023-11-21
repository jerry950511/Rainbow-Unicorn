import pygsheets
import random
gc = pygsheets.authorize(service_file='dinnerchooser-405509-33d9f0bb2be8.json')
sht = gc.open_by_url('https://docs.google.com/spreadsheets/d/1uf7UIUgLfVhhGmEMeGEqa5tdYFZ6gHzeW9Jm3Dzpy-I/edit?usp=sharing')

def get_one_restaurant():
    wks = sht.worksheet_by_title('餐廳選擇器')
    val = wks.get_col(1, include_tailing_empty=False)[1:]
    if len(val) == 0:
        return
    else:
        val = random.choice(val)
        return val

def get_all_restaurant():
    wks = sht.worksheet_by_title('餐廳選擇器')
    val = wks.get_col(1, include_tailing_empty=False)[1:]
    quantity = len(val)
    return val, quantity
    
def add_restaurant(restaurant):
    wks = sht.worksheet_by_title('餐廳選擇器')
    val = wks.get_col(1, include_tailing_empty=False)[1:]
    if restaurant in val:
        return False
    else:
        wks.insert_rows(1, values=[restaurant])
        return True
    
def delete_restaurant(restaurant):
    wks = sht.worksheet_by_title('餐廳選擇器')
    val = wks.get_col(1, include_tailing_empty=False)[1:]
    if restaurant in val:
        wks.delete_rows(val.index(restaurant)+2)
        return True
    else:
        return False
    
