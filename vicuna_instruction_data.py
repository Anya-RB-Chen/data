import os
import json

# Load the data from the json file
FOLDER_PATH = "./PolySmart/data/PolyDepartment_Cleaned_v1"

def load_data(FOLDER_PATH):
    data = []

    for filename in os.listdir(FOLDER_PATH):
        # check if the filename is a directory
        if os.path.isdir(os.path.join(FOLDER_PATH, filename)):
            # check if the directory is empty
            if len(os.listdir(os.path.join(FOLDER_PATH, filename))) == 0:
                continue
            # load the json file in the directory
            for json_file in os.listdir(os.path.join(FOLDER_PATH, filename)):
                if json_file.endswith(".json"):
                    with open(os.path.join(FOLDER_PATH, filename, json_file), encoding='UTF-8') as f:
                        # load each object in the json file
                        count = 0
                        temp_json = json.load(f)
                        for line in temp_json:
                            temp = line
                            temp['id'] = f"{filename}_{count}"
                            data.append(temp)
                            count += 1
            print(f"Loaded {filename}")
    return data


data = load_data(FOLDER_PATH)

# Save the data to a json file， with each object in the list as a line
with open('data_clean.json', 'w') as f:
    for item in data:
        json.dump(item, f)
        f.write('\n')

print("Original dataset saved to data_clean.json")


# ======================== Data Preprocessing ========================

new_data = []

for item in data:
    temp = {}
    temp['id'] = item['id']
    temp['conversations'] = []
    temp_conversation = {}
    temp_conversation['from'] = 'human'
    temp_conversation['value'] = item['text']
    temp['conversations'].append(temp_conversation)
    new_data.append(temp)

    # print the progress
    if len(new_data) % 1000 == 0:
        print(f"Processed {len(new_data)} / {len(data)} data")

# Save the data to a json file
with open('vicuna_instruction_data.json', 'w') as f:
    json.dump(new_data, f)
    
print("New dataset saved to vicuna_instruction_data.json")