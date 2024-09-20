import csv
import os
import glob

# Open the CSV file and extract the data
output_file = 'index.html' # Output file name

# athletes
# womens
# womens_athletes = [{name: [[Overall Place,Grade,Time,Date,Meet,Comments,Photo]]}]
folder_path = 'athletes/womens_team'
womens_athletes = []
csv_files = glob.glob(os.path.join(folder_path, "*.csv"))
for athlete_file in csv_files:
   with open(athlete_file, newline='', encoding='utf-8') as file:
      reader = csv.reader(file)
      name_row = next(reader) 
      athlete_name = name_row[0] 
      next(reader)  # Skip header row (Name,Place,Grade,Time,Date,Meet,Comments,Photo)
      
      athlete_records = []
      # Name,Overall Place,Grade,Time,Date,Meet,Comments,Photo
      for row in reader:
         athlete_records.append({
            "Place": row[1],
            "Grade": row[2],
            "Time": row[3],
            "Date": row[4],
            "Meet": row[5],
            "Comments": row[6],
            "Photo": row[7]
         })
      
      womens_athletes.append({
         athlete_name: athlete_records
      })


# mens
folder_path = 'athletes/mens_team'
mens_athletes = []
csv_files = glob.glob(os.path.join(folder_path, "*.csv"))
for athlete_file in csv_files:
   with open(athlete_file, newline='', encoding='utf-8') as file:
      reader = csv.reader(file)
      name_row = next(reader) 
      athlete_name = name_row[0] 
      next(reader)  # Skip header row (Name,Place,Grade,Time,Date,Meet,Comments,Photo)
      
      athlete_records = []
      # Name,Overall Place,Grade,Time,Date,Meet,Comments,Photo
      for row in reader:
         athlete_records.append({
            "Place": row[1],
            "Grade": row[2],
            "Time": row[3],
            "Date": row[4],
            "Meet": row[5],
            "Comments": row[6],
            "Photo": row[7]
         })
      
      mens_athletes.append({
         athlete_name: athlete_records
      })


# meets
folder_path = 'meets'
meets = []
csv_files = glob.glob(os.path.join(folder_path, "*.csv"))
for meet_file in csv_files:
   # Open one file
   with open(athlete_file, newline='', encoding='utf-8') as file:
      reader = csv.reader(file)
      lines = meet_file.strip().split('\n')
    
      meet_name = lines[0]
      meet_date = lines[1]
      meet_link = lines[2]
      meet_description = lines[3]
      
      meet = {
         'info': [meet_name, meet_date, meet_description],
         'link': meet_link,
         'team_results': [],
         'athlete_results': []
      }
      
      team_scores_start = lines.index("Place,Team,Score") + 1
      athlete_results_start = lines.index("Place,Grade,Name,Athlete Link,Time,Team,Team Link,Profile Pic") + 1
      
      # Parse team scores
      for i in range(team_scores_start, athlete_results_start - 2):
         place, team, score = lines[i].split(',')
         meet['team_results'].append([place, team, score])
      
      # Parse individual athlete results
      for i in range(athlete_results_start, len(lines)):
         # Place,Grade,Name,Athlete Link,Time,Team,Team Link,Profile Pic
         athlete_data = lines[i].split(',')
         place = athlete_data[0].strip('.')
         grade = athlete_data[1]
         name = athlete_data[2]
         link = athlete_data[3]
         time = athlete_data[4]
         team = athlete_data[5]
         team_link = athlete_data[6]
         photo = athlete_data[7]
         meet['athlete_results'].append([place, grade, name, link, time, team, team_link, photo])
      
      meets.append({meet_name: meet})

# images
images = []
images_folder_path = "./images"
for folder in os.listdir(images_folder_path):
   folder_path = os.path.join(images_folder_path, folder)
   if os.path.isdir(folder_path):
      filepaths = []
      for file in os.listdir(folder_path):
         file_path = os.path.join(folder_path, file)
         if os.path.isfile(file_path):  # Make sure it's a file, not a subfolder
            filepaths.append(file_path)
   
   images.append({folder: filepaths})
         

# data structures 
# womens_athletes = [{name: [[Place,Grade,Time,Date,Meet,Comments,Photo]]}]
# mens_athletes = [{name: [[Place,Grade,Time,Date,Meet,Comments,Photo]]}]
# meets = {info: [name, date, link, discription], team_results: [[place, team, score]], athlete_results:[[place, grade, name, athlete, link, time, team, team_link, photo]]]}
# images = {meet: [file1, file2, ...]}

html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
   <meta charset="UTF-8">
   <meta name="viewport" content="width=device-width, initial-scale=1.0">
   <link rel = "stylesheet" href = "css/reset.css">
   <link rel = "stylesheet" href = "css/style.css">
   <title>2024 Race Meets</title>
</head>
<body>

# header Section

   <header>
   <h1>2024-2025 [Insert School]</h1>
      
   </header>
   
   <body>
   <section class="meets">'''
for meet in meets:
      html_content += f'''
      <div class="image-gallery">'''
      if meet.info.name in images:
         html_content += f'''
            <div id="gallery-container" class="gallery-container">
               
      </div>

      <div class="basic-info">
         <h2>{meet.info.name}</h2>
         <p>{meet.info.date}</p>
         <p>{meet.info.description}</p>
         <a href="{meet.link}">Meet Link</a>
         
      </div>

      <div class="team-results">
      <h2>Team Results</h2>'''
      for team_res in meet.team_results:
         html_content += f'''
            <p>{team_res.place}  {team_res.team}   {team_res.score}</p>
         </div>

      <div class="individual-results">
         <h2>Individual Results</h2>'''
      for individual in meet.athlete_results:
         html_content += f'''
         <p>{individual.place}  <a href="{individual.link}">{individual.name}</a>   {individual.time}   <a href="{individual.team_link}">{individual.team}</a></p>
         <img src="{individual.photo}" alt = "athlete headshot">
      </div>
   </section>

   <section class="athlete-list">
      <div class="mens-athletes">
         <h2>Men's Team</h2>'''
      
for athlete in mens_athletes:
   html_content += f'''
            <li>
               <h3>{athlete.name}</h3>
               <p>{athlete.name.place} {athlete.name.grade} {athlete.name.time} {athlete.name.date} {athlete.name.meet} {athlete.name.comments}</p>
               <img src="{athlete.name.photo}" alt="Athlete profile picture">
            </li>
      </div>

      <div class="womens-athletes">
         <h2> Women's Team</h2>'''
         
for athlete in womens_athletes:
   html_content += f'''
               <li>
                  <h3>{athlete.name}</h3>
                  <p>{athlete.name.place} {athlete.name.grade} {athlete.name.time} {athlete.name.date} {athlete.name.meet} {athlete.name.comments}</p>
                  <img src="{athlete.name.photo}" alt="Athlete profile picture">
               </li>
      </div>
   </section>

   <footer>
   </footer>

</body>
</html>
'''

# Save the HTML file
with open(output_file, 'w', encoding='utf-8') as file:
    file.write(html_content)

print(f"{output_file} generated successfully!")