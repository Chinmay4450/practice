import json
import pandas as pd

# Load JSON data
with open("your_file.json", "r") as file:
    data = json.load(file)

# Extract issues from Item1
rows = []
for team_group, group_data in data.items():  # Loop through teams like "Amigos", "Hustle and Flow"
    for entry in group_data:  # Each group can have multiple entries
        item1 = entry.get("Item1")  # Focus only on Item1
        if item1 is None:  # Skip if Item1 is null
            continue
        for team_name, team_data in item1.items():  # Iterate over teams in Item1
            if team_data is None:  # Skip if team data is null
                continue
            try:
                issues = team_data.get("issues", [])  # Extract issues
                for issue in issues:
                    rows.append({
                        "Team": team_name,
                        "Group": team_group,  # e.g., "Amigos" or "Hustle and Flow"
                        "Issue ID": issue.get("id", "N/A"),
                        "Description": issue.get("description", "No description available")
                    })
            except AttributeError:
                # Handle invalid data format
                print(f"Skipping invalid team data for {team_name} in Item1")
                continue

# Convert to DataFrame
df = pd.DataFrame(rows)

# Display or save as CSV
print(df)
df.to_csv("item1_issues_output.csv", index=False)
