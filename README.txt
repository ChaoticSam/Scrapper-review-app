SaaS Review Scraper - Streamlit Application
A Streamlit-based Python application that fetches real-time SaaS product reviews from Capterra, G2, and Trustpilot using the Wextractor API.

This tool allows users to filter reviews by date range, download data in JSON format, and supports pagination for large datasets.

Features
•	Fetches real-time reviews from Capterra, G2, and Trustpilot
•	Extracts correct identifiers from product URLs
•	Filters reviews based on a date range
•	Handles pagination for large datasets
•	Error handling for API failures and incorrect inputs
•	Secure API token management with .env file
•	Allows users to download reviews as JSON

Set Up API Authentication
Create a .env file in the root directory and add your Wextractor API token:
WEXTRACTOR_AUTH_TOKEN=your_api_key_here


Run the Streamlit App
streamlit run app.py


How to Use
1.	Enter the company name
2.	Paste the product review URL
o	Capterra: https://www.capterra.com/p/135003/Slack/
o	G2: https://www.g2.com/products/asana
o	Trustpilot: https://www.trustpilot.com/review/slack.com
3.	Select the review source (Capterra, G2, or Trustpilot)
4.	Choose a date range
5.	Set pagination offset (for large datasets)
6.	Click “Fetch Reviews”
7.	View & Download Reviews in JSON format


API Integration Details
The app uses the Wextractor API to fetch reviews.
Platform	API Endpoint	ID Format
Capterra - /api/v1/reviews/capterra	Extracts id from /p/135003/ in URL
G2 - /api/v1/reviews/g2	Extracts product name from /products/asana in URL
Trustpilot	- /api/v1/reviews/trustpilot	Extracts domain name from /review/slack.com in URL


Troubleshooting
No Reviews Found
•	Try adjusting the date range
•	Ensure correct product URL is used

