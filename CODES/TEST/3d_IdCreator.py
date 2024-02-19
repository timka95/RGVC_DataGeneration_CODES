
import csv
import ast


#INPUT
# filename = 'C:/Users/ASUS/Documents/Timka/Every_data_2.csv'
# filename2 = 'C:/Users/ASUS/Documents/Timka/3D_EveryData.csv'
filename = '/Volumes/TIMKA/NEW_CNN/matfiles/Every_data_2.csv'
filename2 = '/Volumes/TIMKA/NEW_CNN/matfiles/3D_EveryData.csv'


#OUTPUT
filepath = '/Volumes/TIMKA/NEW_CNN/matfiles/3D_EveryDataOUTPUT2.csv'


def read_csv(file_path):
    # Read the CSV file
    with open(file_path, 'r') as csvfile:
        # Create a CSV reader object
        csvreader = csv.reader(csvfile)
        # Get the header
        header = next(csvreader)
        # Create an empty list to store the csvdata
        csvdata = []
        # Iterate over each row in the csv file
        for row in csvreader:
            # Create an empty dictionary
            row_dict = {}
            # Iterate over each cell in the row and the corresponding header cell
            for cell, header_cell in zip(row, header):
                # Add the cell value to the dictionary with the header cell as the key
                row_dict[header_cell] = cell
            # Add the dictionary to the csvdata list
            csvdata.append([row_dict])
        # Return the csvdata list
        return csvdata
    
csvdata = read_csv(filename)
csvdata2 = read_csv(filename2)

savelist = []

for i in range(len(csvdata)):
    csvdata[i] = csvdata[i][0] 
    csvdata[i]["ThetaRho"] = ast.literal_eval(csvdata[i]["ThetaRho"])
    csvdata[i]["2D_orig"] = ast.literal_eval(csvdata[i]["2D_orig"])
    csvdata[i]["2D_376"] = ast.literal_eval(csvdata[i]["2D_376"])
    csvdata[i]["2D_512"] = ast.literal_eval(csvdata[i]["2D_512"])
    csvdata[i]["3D"] = ast.literal_eval(csvdata[i]["3D"])
    csvdata[i]["cuttedhere"] = ast.literal_eval(csvdata[i]["cuttedhere"])



for i in range(len(csvdata2)):
    csvdata2[i] = csvdata2[i][0] 
    csvdata2[i]["id_3D"] = ast.literal_eval(csvdata2[i]["id_3D"])
    csvdata2[i]["3D"] = ast.literal_eval(csvdata2[i]["3D"])
    csvdata2[i]["ID"] = ast.literal_eval(csvdata2[i]["ID"])
    csvdata2[i]["2D_512"] = ast.literal_eval(csvdata2[i]["2D_512"])
    csvdata2[i]["ThetaRho"] = ast.literal_eval(csvdata2[i]["ThetaRho"])

    savelist.append(csvdata2[i])


number = 0
for data in (csvdata2):
    number = number + 1
    if(number % 100 == 0):
        print(len(csvdata2), "-------", number)


print(len(csvdata2))


def process_data(csvdata, csvdata2):
    processed_data = []

    for data in csvdata:
        id_array = []
        new_id_data = {}

        for data_3d in data['3D']:
            for check in csvdata2:
                if check['3D'] == data_3d:
                    new_id = check['id_3D']
                    id_array.append(new_id)

        new_id_data['id_3D'] = id_array
        new_id_data['ID'] = data["ID"]
        new_id_data['2D_512'] = data['2D_512']
        new_id_data['3D'] = data['3D']
        new_id_data['ThetaRho'] = data['ThetaRho']
        processed_data.append(new_id_data)

    return processed_data


def write_data_to_csv(data_array, filename):
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['ID', 'ThetaRho','2D_512', 'id_3D', '3D'  ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for data in data_array:
            writer.writerow(data)




# matching_data = find_matching_data(csvdata, csvdata2)
processed_data = process_data(csvdata, csvdata2)

write_data_to_csv(processed_data, filepath)