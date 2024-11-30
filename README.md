import requests
import pandas as pd


# API details (replace placeholders with actual values)
COMMIT_API_URL = "https://api.example.com/commits"
PULL_REQUEST_API_URL = "https://api.example.com/pull-requests"
API_TOKEN = "your_api_token"

# Headers for API requests
HEADERS = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

# Function to fetch commits by author
def fetch_commits(author):
    try:
        response = requests.get(
            COMMIT_API_URL,
            headers=HEADERS,
            params={"author": author},
            timeout=10  # Set timeout to prevent hanging requests
        )
        response.raise_for_status()  # Raise exception for HTTP errors
        return response.json()  # Parse JSON if successful
    except requests.exceptions.RequestException as e:
        print(f"Error fetching commits for {author}: {e}")
        return []  # Return an empty list if there's an error

# Function to check if a commit is linked to a pull request
def check_pull_request(commit_id):
    try:
        response = requests.get(
            f"{PULL_REQUEST_API_URL}/{commit_id}",
            headers=HEADERS,
            timeout=10  # Set timeout to prevent hanging requests
        )
        response.raise_for_status()  # Raise exception for HTTP errors
        return response.json()  # Parse JSON if successful
    except requests.exceptions.RequestException as e:
        print(f"Error checking pull request for commit ID {commit_id}: {e}")
        return None  # Return None if there's an error

# Flatten data for CSV and fetch API data
csv_data = []

for team in teams_data:
    team_name = team.get("TeamName", "Unknown Team")  # Handle missing team name
    for member in team.get("Members", []):  # Handle missing members list
        # Fetch commits for the member
        commits = fetch_commits(member)
        if commits:
            for commit in commits:
                commit_id = commit.get("id", "None")
                message = commit.get("message", "No message provided")
                pull_request = check_pull_request(commit_id)
                pull_request_id = pull_request.get("id") if pull_request else "None"
                pull_request_status = pull_request.get("status") if pull_request else "None"
                
                # Append commit details
                csv_data.append({
                    "Team Name": team_name,
                    "Author": member,
                    "Commit ID": commit_id,
                    "Message": message,
                    "Pull Request ID": pull_request_id,
                    "Pull Request Status": pull_request_status
                })
        else:
            # If no commits found
            csv_data.append({
                "Team Name": team_name,
                "Author": member,
                "Commit ID": "None",
                "Message": "No commits found",
                "Pull Request ID": "None",
                "Pull Request Status": "None"
            })

# Convert the list of dictionaries to a pandas DataFrame
df = pd.DataFrame(csv_data)

# Save the DataFrame to a CSV file
csv_file_path = "team_commits_with_pandas.csv"
df.to_csv(csv_file_path, index=False)

print(f"CSV file created successfully at: {csv_file_path}")
