import streamlit as st
import requests
import pandas as pd


# Function to fetch all deployments
@st.cache_data
def fetch_deployments(api_token):
    deployments = []
    next_url = "https://api.replicate.com/v1/deployments"
    headers = {"Authorization": f"Token {api_token}"}

    while next_url:
        response = requests.get(next_url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            deployments.extend(data['results'])
            next_url = data.get('next')  # Update the next_url for the next iteration
        else:
            st.error("Failed to fetch deployments. Please check your API token and try again.")
            break

    return deployments

st.set_page_config(layout='wide')

# Streamlit UI
st.title('🚀 Replicate Deployments Viewer')

# Sidebar for API token input
api_token = st.sidebar.text_input("Enter your Replicate API Token:", type="password")

# Sidebar checkboxes for toggling columns
columns = ["Owner", "Name", "Date Created", "Model", "Version", "Created By", "Hardware", "Min Instances", "Max Instances",
           "Replicate URL"]
selected_columns = []
for column in columns:
    if st.sidebar.checkbox(f"Show {column}", True):
        selected_columns.append(column)

if api_token:
    # Fetch deployments
    deployments = fetch_deployments(api_token)

    if deployments:
        # Process and prepare the data for display
        data = []
        for deployment in deployments:
            current_release = deployment['current_release']
            print(current_release)
            data.append({
                "Owner": deployment['owner'],
                "Name": deployment['name'],
                "Date Created": current_release['created_at'],
                "Model": current_release['model'],
                "Version": current_release['version'],
                "Created By": current_release['created_by']['name'],
                "Hardware": current_release['configuration']['hardware'],
                "Min Instances": current_release['configuration']['min_instances'],
                "Max Instances": current_release['configuration']['max_instances'],
                "Replicate URL": f"https://replicate.com/deployments/{deployment['owner']}/{deployment['name']}"
            })

        df = pd.DataFrame(data)

        # Display the DataFrame as a table with selected columns
        if selected_columns:
            st.dataframe(df[selected_columns])
        else:
            st.warning("Please select at least one column to display.")

else:
    st.sidebar.warning("Please enter your API token to view deployments.")
