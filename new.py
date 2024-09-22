import os
import csv

# Specify the directory containing the CSV files
directory = "/Users/filiphendl/Desktop/339_F2024/SI339D2/"

# List all files in the directory and its subdirectories
csv_files = []

for root, dirs, files in os.walk(directory):
    for file in files:
        if file.endswith('.csv'):
            csv_files.append(os.path.join(root, file))

print("CSV Files in Directory and Subdirectories:", csv_files)

# Check if there are any CSV files in the directory
if not csv_files:
    print("No CSV files found in the directory and its subdirectories.")
    exit()  # Exit the script if no CSV files are found

# Select the first CSV file in the list for processing
csv_file = csv_files[0]
print(f"Processing CSV File: {csv_file}")



# Open the CSV file and extract the data
with open(csv_files, newline='', encoding='utf-8') as file:
   reader = csv.reader(file)
   data = list(reader)
   print(data[0])


# Extract the data from the CSV
meet_name = data[1][0]  # Column A - h1 (Meet Name)
meet_date = data[1][1]  # Column B - h2 (Meet Date)
team_results_link = data[1][2]  # Column C - hyperlink for the team-results section
folder_name = data[1][3]  # Column D - folder name used in photo-gallery links
race_comments = data[1][4]  # Column E - race-comments section


print(f"meet name {meet_name}")
print(f"meet_date {meet_date}")
print(f"folder_name {folder_name}")
print(f"race_comments{race_comments}")


# Athlete details start from row 2 (index 1)
athletes = data[1:]


# Start building the HTML structure
html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
   <meta charset="UTF-8">
   <meta name="viewport" content="width=device-width, initial-scale=1.0">
   <link rel = "stylesheet" href = "css/reset.css">
   <link rel = "stylesheet" href = "css/style.css">
   <title>{meet_name} Country Meet</title>
</head>
<body>
   <header>
       <h1>{meet_name}</h1>
       <h2>{meet_date}</h2>
   </header>
'''
html_content += f'''
    <section id= "team-results">
        <h2>Overall Team Results</h2>
        <p><a href="{team_results_link}">Team results are available here.</a></p>
    </section>
'''
        
html_content += '''
    <section id= "athlete-results">
        <h2>Athlete Results</h2>
        <table id = "athlete-table">
            <thead>
                </tr>
                    <th>Name</th>
                    <th>Time</th>
                    <th>Place</th>
                    <th>Image</th>
                    <th>Feedback</th>
                </tr>
            </thead>
            <tbody>
            
'''
for athlete in athletes:
    athlete_name = athlete[5]
    athlete_place = athlete[7] #add corrisponding numbers where they should go 
    athlete_time = athlete[8]
    athlete_image = athlete[6]
    athlete_feedback = athlete[9]


    html_content += f'''
                <tr>
                    <td>{athlete_name}</td>
                    <td>{athlete_time}</td>
                    <td>{athlete_place}</td>
                    <td><img src="images/{athlete_image}" alt="{athlete_name}" width="100"></td>
                    <td>{athlete_feedback}</td>
                </tr>
    '''

# clsing the table of athlete section 

html_content += '''
            </tbody>
        </table>
    </section>
'''

# adding a footer section
html_content += f'''
    <footer>
        <p>Coach Comments: {race_comments}</p>
    </footer>
</body>
</html>
'''

output_file = "LamplighterInvite23.html"
with open(output_file, 'w', encoding ='utf-8') as file:
    file.write(html_content)

print(f"HTML file {output_file} created successfully.")
