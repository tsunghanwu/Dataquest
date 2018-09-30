file = open("AviationData.txt", "r")
aviation_data = file.readlines()
aviation_list = []
for row in aviation_data:
    aviation_list.append(row.split(" | "))

lax_code = []
for row in aviation_list:
    for item in row:
        if item == "LAX94LA336":
            lax_code.append(row)

aviation_dict_list = []
header = aviation_list[0]
data = aviation_list[1:]
for row in data:
    aviation_dict = {}
    for index, item in enumerate(row):
        aviation_dict[header[index]] = item
    aviation_dict_list.append(aviation_dict)

state_accidents = {}
for row in aviation_dict_list:
    if row["Country"] == "United States" and row["Investigation Type"] == "Accident":
        if row["Location"] != "":
            split_loc = row["Location"].split(", ")
            state = split_loc[1]
            if state in state_accidents.keys():
                state_accidents[state] += 1
            else:
                state_accidents[state] = 1

max_key = "TX"

for key in state_accidents.keys():
    if state_accidents[key] > state_accidents[max_key]:
        max_key = key

print(max_key, state_accidents[max_key])

monthly_injuries = {}
for row in aviation_dict_list:
    if row["Event Date"] != "" and row["Total Fatal Injuries"] != "" and row["Total Serious Injuries"] != "":
        month = row["Event Date"].split("/")[0]
        total = int(row["Total Fatal Injuries"]) + int(row["Total Serious Injuries"])
        if month in monthly_injuries.keys():
                monthly_injuries[month] += total
        else:
            monthly_injuries[month] = total
                
max_key = "01"
for key in monthly_injuries.keys():
    if monthly_injuries[key] > monthly_injuries[max_key]:
        max_key = key
        
print(max_key, monthly_injuries[max_key])
