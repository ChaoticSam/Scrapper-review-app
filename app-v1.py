# import streamlit as st
# import pandas as pd
# import requests
# import os
# import json
# from dotenv import load_dotenv
# from datetime import datetime

# # Load API token from .env file
# load_dotenv()
# # AUTH_TOKEN = os.getenv("WEXTRACTOR_AUTH_TOKEN")
# AUTH_TOKEN = "9d6a94f93a936606446d3812fe964d16aa4c929b"

# # API Endpoints
# API_ENDPOINTS = {
#     "Capterra": "https://wextractor.com/api/v1/reviews/capterra",
#     "G2": "https://wextractor.com/api/v1/reviews/g2",
#     "Trustpilot": "https://wextractor.com/api/v1/reviews/trustpilot"
# }

# # Function to extract the software identifier from the given URL
# def extract_identifier(source, url):
#     try:
#         if source == "Capterra" or source == "G2":
#             # Capterra and G2 URLs follow format: https://www.capterra.com/p/135003/Slack/
#             return url.split('/p/')[1].split('/')[0]
#         elif source == "Trustpilot":
#             # Trustpilot URLs follow format: https://www.trustpilot.com/review/slack.com
#             return url.split("/review/")[1]  # Extracts "slack.com"
#         else:
#             return None
#     except IndexError:
#         return None

# # Function to fetch reviews from Wextractor API
# def fetch_reviews(source, identifier, offset=0):
#     url = API_ENDPOINTS[source]
#     params = {
#         "id" if source in ["Capterra", "G2"] else "domain": identifier,  # Trustpilot uses "domain"
#         "auth_token": AUTH_TOKEN,
#         "offset": offset
#     }
    
#     try:
#         response = requests.get(url, params=params, timeout=15)
#         if response.status_code == 200:
#             return response.json().get("reviews", [])
#         elif response.status_code == 400:
#             st.error("Bad Request: Check the identifier or API token.")
#         elif response.status_code == 403:
#             st.error("Forbidden: Invalid API token.")
#         elif response.status_code == 429:
#             st.error("Rate limit exceeded. Try again later.")
#         elif response.status_code == 500:
#             st.error("Server Error: The API is experiencing issues. Try later.")
#         else:
#             st.error(f"Unexpected Error: {response.status_code}")
#         return []
    
#     except requests.exceptions.Timeout:
#         st.error("API Request Timed Out. Try again.")
#         return []
#     except requests.exceptions.RequestException as e:
#         st.error(f"Request Failed: {e}")
#         return []

# # Function to filter reviews by date range
# def filter_reviews_by_date(reviews, start_date, end_date):
#     filtered_reviews = []
#     for review in reviews:
#         try:
#             # Extract only the date part and handle "T" in datetime format
#             review_date_str = review["datetime"].split("T")[0]  
#             review_date = datetime.strptime(review_date_str, "%Y-%m-%d")

#             if start_date <= review_date <= end_date:
#                 filtered_reviews.append({
#                     "title": review.get("title", "No Title"),
#                     "description": review.get("text", "No Description"),
#                     "date": review_date_str,
#                     "reviewer": review.get("reviewer", "Anonymous"),
#                     "rating": review.get("rating", "N/A")
#                 })

#         except Exception as e:
#             st.error(f"Error processing review date: {e}")
    
#     return filtered_reviews

# # Streamlit App UI
# st.title("📊 SaaS Review Extractor (Capterra, G2, Trustpilot)")

# # User Inputs
# company_name = st.text_input("Enter Company Name:")
# software_url = st.text_input("Enter the Software Review URL:")
# start_date = st.date_input("Start Date")
# end_date = st.date_input("End Date")
# source = st.radio("Select Review Source:", ["Capterra", "G2", "Trustpilot"], index=0)

# # Fetch Reviews Button
# if st.button("Fetch Reviews"):
#     if AUTH_TOKEN and company_name and software_url and start_date and end_date:
#         try:
#             # Extract the correct identifier based on the selected source
#             identifier = extract_identifier(source, software_url)

#             if identifier:
#                 reviews = fetch_reviews(source, identifier)

#                 if reviews:
#                     # Convert start_date and end_date to datetime
#                     start_date_dt = datetime.combine(start_date, datetime.min.time())
#                     end_date_dt = datetime.combine(end_date, datetime.min.time())

#                     # Filter reviews within the given date range
#                     filtered_reviews = filter_reviews_by_date(reviews, start_date_dt, end_date_dt)

#                     if filtered_reviews:
#                         df = pd.DataFrame(filtered_reviews)
#                         st.write(f"### {source} Reviews for {company_name}")
#                         st.dataframe(df)

#                         # Prepare JSON Output
#                         json_data = json.dumps(filtered_reviews, indent=4)
#                         st.download_button(
#                             label="Download Reviews as JSON",
#                             data=json_data,
#                             file_name=f"{company_name}_{source}_reviews.json",
#                             mime="application/json"
#                         )
#                     else:
#                         st.warning("No reviews found in the selected date range.")
                
#                 else:
#                     st.warning("No reviews found. Check the software URL or API token.")
#             else:
#                 st.error("Invalid software URL format. Please enter a correct link.")

#         except IndexError:
#             st.error("Error extracting software identifier. Ensure the URL format is correct.")
#     else:
#         st.warning("Please provide all required inputs.")


import streamlit as st
import pandas as pd
import requests
import os
import json
from dotenv import load_dotenv
from datetime import datetime

# Load API token from .env file
load_dotenv()
AUTH_TOKEN = os.getenv("WEXTRACTOR_AUTH_TOKEN")

# API Endpoints
API_ENDPOINTS = {
    "Capterra": "https://wextractor.com/api/v1/reviews/capterra",
    "G2": "https://wextractor.com/api/v1/reviews/g2",
    "Trustpilot": "https://wextractor.com/api/v1/reviews/trustpilot"
}

# Function to extract the correct identifier from the URL
def extract_identifier(source, url):
    try:
        if source == "Capterra":
            return url.split('/p/')[1].split('/')[0]  # Extracts numeric ID from URL
        elif source == "G2":
            return url.split('/products/')[1].split('/')[0]  # Extracts product name
        elif source == "Trustpilot":
            return url.split("/review/")[1]  # Extracts domain name
        else:
            return None
    except IndexError:
        return None

# Function to fetch reviews from the API
def fetch_reviews(source, identifier, offset=0):
    url = API_ENDPOINTS[source]
    params = {
        "id": identifier,
        "auth_token": AUTH_TOKEN,
        "offset": offset
    }

    try:
        response = requests.get(url, params=params, timeout=15)
        if response.status_code == 200:
            return response.json().get("reviews", [])
        elif response.status_code == 400:
            st.error("Bad Request: Check the identifier or API token.")
        elif response.status_code == 403:
            st.error("Forbidden: Invalid API token.")
        elif response.status_code == 429:
            st.error("Rate limit exceeded. Try again later.")
        elif response.status_code == 500:
            st.error("Server Error: The API is experiencing issues. Try later.")
        else:
            st.error(f"Unexpected Error: {response.status_code}")
        return []
    
    except requests.exceptions.Timeout:
        st.error("API Request Timed Out. Try again.")
        return []
    except requests.exceptions.RequestException as e:
        st.error(f"Request Failed: {e}")
        return []

# Function to filter reviews by date range
from datetime import datetime

def filter_reviews_by_date(reviews, start_date, end_date):
    filtered_reviews = []
    for review in reviews:
        try:
            # Extract only the date part, handling both "T" and space-separated formats
            review_date_str = review["datetime"].split("T")[0] if "T" in review["datetime"] else review["datetime"].split(" ")[0]
            review_date = datetime.strptime(review_date_str, "%Y-%m-%d")

            if start_date <= review_date <= end_date:
                filtered_reviews.append({
                    "title": review.get("title", "No Title"),
                    "description": review.get("text", "No Description"),
                    "date": review_date_str,
                    "reviewer": review.get("reviewer", "Anonymous"),
                    "rating": review.get("rating", "N/A")
                })

        except Exception as e:
            st.error(f"Error processing review date: {e}")
    
    return filtered_reviews


# Streamlit App UI
st.title("📊 SaaS Review Extractor (Capterra, G2, Trustpilot)")

# User Inputs
company_name = st.text_input("Enter Company Name:")
software_url = st.text_input("Enter the Software Review URL:")
start_date = st.date_input("Start Date")
end_date = st.date_input("End Date")
source = st.radio("Select Review Source:", ["Capterra", "G2", "Trustpilot"], index=0)

# Pagination offset input
offset = st.number_input("Offset for Pagination (Default: 0)", min_value=0, step=10)

# Fetch Reviews Button
if st.button("Fetch Reviews"):
    if AUTH_TOKEN and company_name and software_url and start_date and end_date:
        try:
            # Extract the correct identifier based on the selected source
            identifier = extract_identifier(source, software_url)

            if identifier:
                reviews = fetch_reviews(source, identifier, offset)

                if reviews:
                    # Convert start_date and end_date to datetime
                    start_date_dt = datetime.combine(start_date, datetime.min.time())
                    end_date_dt = datetime.combine(end_date, datetime.min.time())

                    # Filter reviews within the given date range
                    filtered_reviews = filter_reviews_by_date(reviews, start_date_dt, end_date_dt)

                    if filtered_reviews:
                        df = pd.DataFrame(filtered_reviews)
                        st.write(f"### {source} Reviews for {company_name}")
                        st.dataframe(df)

                        # Prepare JSON Output
                        json_data = json.dumps(filtered_reviews, indent=4)
                        st.download_button(
                            label="Download Reviews as JSON",
                            data=json_data,
                            file_name=f"{company_name}_{source}_reviews.json",
                            mime="application/json"
                        )
                    else:
                        st.warning("No reviews found in the selected date range.")
                
                else:
                    st.warning("No reviews found. Check the software URL or API token.")
            else:
                st.error("Invalid software URL format. Please enter a correct link.")

        except IndexError:
            st.error("Error extracting software identifier. Ensure the URL format is correct.")
    else:
        st.warning("Please provide all required inputs.")
