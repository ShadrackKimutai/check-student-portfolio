import requests
from bs4 import BeautifulSoup
import pandas as pd  # For creating dataframes


# Moodle site details
moodle_url = "https://steveomenge.gnomio.com/"
login_page = moodle_url + "/login/index.php"

# User credentials
username = "trainer"
password = "Odel@2022"

# Session object for persistent cookies
session = requests.Session()

# Get login page to capture hidden tokens
response = session.get(login_page)
soup = BeautifulSoup(response.content, "html.parser")

# Extract hidden tokens, if present
logintoken = soup.find("input", {"name": "logintoken"}).get("value")
sesskey = soup.find("input", {"name": "sesskey"}).get("value")

# Login data (adapt if additional fields are required)
login_data = {
    "username": username,
    "password": password,
    "logintoken": logintoken,
    "sesskey": sesskey
}

# Send login POST request
response = session.post(login_page, data=login_data)

# Check for successful login
if response.url == moodle_url:
    print("Login successful!")
    # Navigate to desired pages or perform actions using session.get() or session.post()
else:
    print("Login failed. Please check credentials and tokens.")

    #try taking snaps of Home page



# ... (Login code from the previous script)

# Navigate to courses page after successful login
courses_page = moodle_url + "/course/index.php"
response = session.get(courses_page)

# Parse course information
soup = BeautifulSoup(response.content, "html.parser")

# Extract course data (adapt selectors based on Moodle's structure)
course_data = []
for course_element in soup.find_all("li", class_="coursebox"):
    title_element = course_element.find("h3", class_="coursename")
    if title_element:
        title = title_element.text.strip()
    else:
        title = "Untitled Course"  # Handle missing titles gracefully
    link = course_element.find("a")["href"]
    enrollment = course_element.find("span", class_="enrolmenticons").text.strip()
    course_data.append({"title": title, "link": link, "enrollment": enrollment})

# Create a DataFrame for organized presentation
courses_df = pd.DataFrame(course_data)
print(courses_df)

# Optional: Save snapshot to a CSV file
courses_df.to_csv("moodle_courses_snapshot.csv", index=False)



