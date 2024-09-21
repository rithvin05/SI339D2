# HTML template
html_main = '''<!DOCTYPE html>
<html lang="en">
<head>  
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ann Arbor Skyline Meets</title>
</head>
<body>
    <header>
        <h1>Ann Arbor Skyline</h1>
    </header>
    <section id="meetList">
        <h2>Meets</h2>
        <table id="meet-table">
            <tbody>
                {meet_rows}
            </tbody>
        </table>
    </section>
    
    <section id="Roster">
        <h2>Roster</h2>
        <h3>Women's Team</h3>
        <table id="women-table">
            <thead>
                <tr>
                    <th>Name</th>
                </tr>
            </thead>
            <tbody>
                {womens_rows}
            </tbody>
        </table>

        <h3>Men's Team</h3>
        <table id="men-table">
            <thead>
                <tr>
                    <th>Name</th>
                </tr>
            </thead>
            <tbody>
                {mens_rows}
            </tbody>
        </table>
    </section>

    
</body>
</html>    
'''

html_template = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="css/reset.css">
    <link rel="stylesheet" href="css/style.css">
    <title>{meet_name} Country Meet</title>
</head>
<body>
    <header>
        <h1>{meet_name}</h1>
        <h2>{meet_date}</h2>
        <p>{meet_desc}</p>
    </header>
    <!-- Section for overall team results -->
    <section id="team-results">
        <h2>Overall Team Results</h2>
        <p><a href="{team_results_link}">Team results are available here.</a></p>
    </section>
    <!-- Section for athlete table -->
    <section id="athlete-results">
        <h2>Athlete Results</h2>
        <table id="athlete-table">
            <thead>
                <tr>
                    <th>Place</th>
                    <th>Name</th>
                    <th>Time</th>
                    <th>Grade</th>
                    <th>Team</th>            
                </tr>
            </thead>
            <tbody>
                {athlete_rows}
            </tbody>
        </table>
    </section>
</body>
</html>
'''

import csv
import os
import re


# Define file names

main_file = "index.html"

    
# Function to generate HTML content based on CSV data

def generate_html_from_csv(csv_file, output_file):
    with open(csv_file, newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        data = list(reader)
        
        # Extract event data from the CSV
        meet_name = data[0][0]  # Column A - Meet Name
        meet_date = data[1][0]  # Column B - Meet Date
        team_results_link = data[2][0]  # Column C - hyperlink for the team-results section
        meet_desc = data[3]  # Column D - Meet Description
        
        header_index = 0
        for i, row in enumerate(data):
            if row and row[0].strip().lower() == 'place':  # Assuming the first column contains 'Place'
                header_index = i

        # Generate athlete rows
        athlete_rows = ""
        for athlete in data[header_index + 1:]:  # Start from the third row (ignoring header rows)
            athlete_place = athlete[0]  # Column G - athlete-place
            athlete_grade = athlete[1] # Column E - athlete-grade
            athlete_name = athlete[2]  # Column F - athlete-name
            athlete_link = athlete[3]   # Column G - athlete-link
            athlete_time = athlete[4]  # Column H - athlete-time
            athlete_team = athlete[5]  # Column H - athlete-team
            # athlete_image = athlete[7]  # Column I - athlete-image
            # athlete_feedback = athlete[9]  # Column J - athlete-feedback
            
            # Format the row for each athlete
            athlete_rows += f'''
                <tr>
                    <td>{athlete_place}</td>
                    <td><a href="{athlete_link}">{athlete_name}</a></td>
                    <td>{athlete_time}</td>
                    <td>{athlete_grade}</td>
                    <td>{athlete_team}</td>
                
                </tr>
            '''
        
        # Replace placeholders in the HTML template
        html_content = html_template.format(
            meet_name=meet_name,
            meet_date=meet_date,
            team_results_link=team_results_link,
            athlete_rows=athlete_rows,
            meet_desc=meet_desc
        )

        
        # Write the HTML content to a file
        with open(output_file, 'w', encoding='utf-8') as output:
            output.write(html_content)

meet_rows = ""
mens_rows = ""
womens_rows = ""

for filename in os.listdir('meets'):
    if filename.endswith('.csv'):
        csv_file = os.path.join('meets', filename)
        name1 = filename[:-4]
        output_file = re.sub(r'[^a-zA-Z0-9_]', '', name1.lower().replace(" ", "_")) + '.html'

        # output_file = f"{filename[:-4]}.html"  # Remove the .csv extension
        generate_html_from_csv(csv_file, output_file)
        print(f"Generated: {output_file}")
        name = f"{filename[:-4]}".replace("_", " ")
        meet_rows += f'''
                <tr>
                    <td><a href="{output_file}">{name}</a></td>
                    
                </tr>
            '''
for filename in os.listdir('athletes/mens_team'):
    if filename.endswith('.csv'):
        csv_file = os.path.join('athletes/mens_team', filename)
    with open(csv_file, newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        data = list(reader)
        mens_rows += f'''
                <tr>
                    <td>{data[5][0]}</td>
                </tr>
            '''
for filename in os.listdir('athletes/womens_team'):
    if filename.endswith('.csv'):
        csv_file = os.path.join('athletes/womens_team', filename)
    with open(csv_file, newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        data = list(reader)
        womens_rows += f'''
                <tr>
                    <td>{data[5][0]}</td>
                </tr>
            '''
        

html_main_content = html_main.format(
    meet_rows=meet_rows,
    womens_rows=womens_rows,
    mens_rows=mens_rows
)

with open(main_file, 'w', encoding='utf-8') as output:
            output.write(html_main_content)

        

# Generate the HTML file from the CSV data