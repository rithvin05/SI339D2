import os
import csv

# Function to read athlete data from CSV files and build a dictionary
def load_athlete_data(directory):
    athlete_data = {}
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.csv'):
                file_path = os.path.join(root, file)
                with open(file_path, newline='', encoding='utf-8') as csvfile:
                    reader = csv.DictReader(csvfile)
                    # Skip files with no 'Name' column
                    if 'Name' not in reader.fieldnames:
                        continue

                    for row in reader:
                        name = row['Name'].strip()
                        if name not in athlete_data:
                            athlete_data[name] = []
                        
                        athlete_data[name].append({
                            'overall_place': row.get('Overall Place', '').strip(),
                            'grade': row.get('Grade', '').strip(),
                            'time': row.get('Time', '').strip(),
                            'date': row.get('Date', '').strip(),
                            'meet_name': row.get('Meet', '').strip(),
                            'comments': row.get('Comments', '').strip(),
                            'photo': row.get('Photo', '').strip()
                        })
    return athlete_data

# Function to generate the HTML content dynamically
def generate_html(roster_data):
    html_content = '''<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>XC Team and Meet Info</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            h1, h2 { text-align: center; }
            table { width: 100%; border-collapse: collapse; margin-bottom: 20px; }
            th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
            th { background-color: #f2f2f2; }
            tr:hover { background-color: #f5f5f5; }
            .expandable { cursor: pointer; color: blue; text-decoration: underline; }
            .hidden { display: none; }
        </style>
        <script>
            function toggleVisibility(id) {
                var element = document.getElementById(id);
                if (element.classList.contains('hidden')) {
                    element.classList.remove('hidden');
                } else {
                    element.classList.add('hidden');
                }
            }
        </script>
    </head>
    <body>
        <h1>XC Team and Meet Information</h1>
        <section id="roster">
            <h2>Roster of XC Team</h2>
            <table>
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Overall Place</th>
                        <th>Grade</th>
                        <th>Best Time</th>
                        <th>Expand</th>
                    </tr>
                </thead>
                <tbody>
    '''
    
    for name, events in roster_data.items():
        # Calculate best time and summary info
        best_time = min([event['time'] for event in events if event['time']])
        overall_place = events[0]['overall_place']
        grade = events[0]['grade']
        comments = events[0]['comments']

        # Main row for athlete
        html_content += f'''
                    <tr>
                        <td><span class="expandable" onclick="toggleVisibility('{name.replace(" ", "_")}_details')">{name}</span></td>
                        <td>{overall_place}</td>
                        <td>{grade}</td>
                        <td>{best_time}</td>
                        <td>Click to expand</td>
                    </tr>
                    <tr id="{name.replace(" ", "_")}_details" class="hidden">
                        <td colspan="5">
                            <table>
                                <thead>
                                    <tr>
                                        <th>Date</th>
                                        <th>Meet Name</th>
                                        <th>Time</th>
                                        <th>Comments</th>
                                        <th>Photo</th>
                                    </tr>
                                </thead>
                                <tbody>
        '''
        # Event details for this athlete
        for event in events:
            html_content += f'''
                                    <tr>
                                        <td>{event['date']}</td>
                                        <td>{event['meet_name']}</td>
                                        <td>{event['time']}</td>
                                        <td>{event['comments']}</td>
                                        <td><img src="{event['photo']}" alt="{name}" width="100"></td>
                                    </tr>
            '''
        html_content += '''
                                </tbody>
                            </table>
                        </td>
                    </tr>
        '''
    
    # Closing the roster section
    html_content += '''
                </tbody>
            </table>
        </section>
    </body>
    </html>
    '''

    return html_content

# Main function
def main():
    # Directory containing athlete CSV files
    athletes_directory = "/Users/filiphendl/Desktop/339_F2024/SI339D2/athletes/"
    
    # Load athlete data
    roster_data = load_athlete_data(athletes_directory)
    
    # Generate HTML content
    html_content = generate_html(roster_data)
    
    # Save to an HTML file
    output_file = "XC_Team_Info.html"
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(html_content)

    print(f"HTML file {output_file} created successfully.")

    # Print the current working directory before saving the HTML file
    print("Current Working Directory:", os.getcwd())

# Run the main function
if __name__ == "__main__":
    main()
