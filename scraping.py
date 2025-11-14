import requests
import csv
from bs4 import BeautifulSoup
from collections import Counter
import matplotlib.pyplot as plt


base_url = "https://libyanjobs.ly/jobs/?s=&location=&post_type=noo_job"
# CSV file setup
csv_file_path = 'job_details.csv'

with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file) #This object to write rows into the CSV file
    writer.writerow(['Job Title', 'Job Type', 'location','Company Name', 'Deadline', 'Posting Date', 'Applications', 'Views', 'Years of Experience'])  # Writing the header row

    # Loop through pages 1 to 17 and scrape job details
    for page in range(1, 60):
        page_url = f"{base_url}&paged={page}"   #construct the URL for a specific page of job listings
        response = requests.get(page_url) #send an HTTP GET request to the page_url
        soup = BeautifulSoup(response.content, 'html.parser') #create a BeautifulSoup object
        #response.content, is the raw HTML content of the web page


        job_listings = soup.find_all('div', class_='loop-item-wrap') #search for and return a list of all <div> with a class name of 'loop-item-wrap'
                                                                      #The job_listings variable holds a list of Tag
        for job in job_listings:
            title = job.find('h3', class_='loop-item-title')
            job_type = job.find('span', class_='job-type')
            company_name = job.find('span', class_='job-company')
            location=job.find('span', class_='job-location')
            deadline = job.find('span', class_='job-date')
            posting_date = job.find('span', class_='job-date-ago')
            applications = job.find('span', class_=['count', 'applications'])
            views = job.find('span', class_=['count', 'views'])
            years_experience = job.find('strong', class_=lambda x: x and 'experience_year' in x)

            # Extract the text or set 'N/A' if the element is not found
            title_text = title.text.strip() if title else 'N/A'
            job_type_text = job_type.text.strip() if job_type else 'N/A'
            company_name_text = company_name.text.strip() if company_name else 'N/A'
            location_text=location.text.strip() if location else 'N/A'
            deadline_text = deadline.text.strip() if deadline else 'N/A'
            posting_date_text = posting_date.text.strip() if posting_date else 'N/A'
            applications_text = applications.text.strip() if applications else 'N/A'
            views_text = views.text.strip() if views else 'N/A'
            years_experience_text = years_experience.text.strip() if years_experience else 'N/A'

            writer.writerow([title_text, job_type_text,location_text ,company_name_text, deadline_text, posting_date_text, applications_text, views_text, years_experience_text])

print(f"Job details scraped and saved to {csv_file_path}")