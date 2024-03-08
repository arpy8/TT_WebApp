import os
import random
import string
from pymongo import MongoClient

mongo_url = os.environ["mongo_url"]
db_name = os.environ["db_name"]
records_name = os.environ["records_name"]

client = MongoClient(mongo_url)
db = client.get_database(db_name)
records = db.get_collection(records_name)

def remove_duplicates(input_str):
    unique_chars = []
    result_str = ""

    for char in input_str:
        if char not in unique_chars:
            unique_chars.append(char)
            result_str += char

    return result_str

def get_all_tt_ids():
    tt_ids = records.distinct("tt_id")
    return tt_ids
     
def add_time_table(name, emoji, tt_slots):
    tt_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 6))
    data = {
        "tt_id": tt_id,
        tt_id:{
            name:{
                "emoji": emoji,
                "tt_slots": tt_slots
            }
        }
    }
    
    try:
        records.insert_one(data)
        print("Inserting: ", data)
        
        return tt_id
    
    except Exception as e:
        return f"Error: {e}"

def update_time_table(tt_id, name, emoji, tt_slots):
    try:
        record = records.find_one({"tt_id": tt_id})

        if record:
            records.update_one(
                {"tt_id": tt_id},
                {
                    "$set": {
                        f"{tt_id}.{name}": {
                            "emoji": emoji,
                            "tt_slots": tt_slots
                        }
                    }
                },
                upsert=True
            )

            return f"{name} has been added to time table: {tt_id} successfully."
        else:
            return f"Error: Timetable with ID {tt_id} not found."

    except Exception as e:
        return f"Error: {e}"
        
def authenticate_tt_id(tt_id):
    try:
        return tt_id in get_all_tt_ids()
    except Exception as e:
        return f"Error: {e}"

def fetch_tt_data(tt_id):
    query = {tt_id: {"$exists": True}}
    documents = records.find(query)

    temp_list = []
    for document in documents:
        temp_list.append(document)
    return temp_list

if __name__=="__main__":
    # tt_id = add_time_table("test_user", "😭", ['A11', 'B11', 'C11',"sdasd", "sdada"])
    # print(update_time_table("V3IOGQ", "user_{i}", "😭", ['aaa{i}', 'BBB{i+1}', 'CCC{i+2}']))
    print(get_all_tt_ids())
    # print(get_all_tt_ids())
    # print(fetch_tt_data("121212"))