import re
import pandas as pd
from datetime import datetime
import os

def extract_dates_times():
    # File paths
    input_file = r"C:\Users\user\OneDrive\Desktop\BKS\project\trans_capture.txt"
    output_file = r"C:\Users\user\OneDrive\Desktop\BKS\project\extracted_dates_times.xlsx"
    
    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"Error: Input file {input_file} not found.")
        return
    
    # Read the transcription file
    with open(input_file, 'r') as file:
        lines = file.readlines()
    
    # Lists to store extracted data
    entry_timestamps = []
    extracted_dates = []
    extracted_texts = []
    
    # Regular expressions for date extraction
    # Pattern for dates like "18th of March 2020" or "18th March 2020"
    date_pattern1 = r'(\d{1,2})(?:st|nd|rd|th)?\s+(?:of\s+)?([A-Za-z]+)\s+(\d{4})'
    # Pattern for dates like "March 18, 2020" or "March 18 2020"
    date_pattern2 = r'([A-Za-z]+)\s+(\d{1,2})(?:,|\s)\s*(\d{4})'
    # Pattern for dates like "18/03/2020" or "18-03-2020"
    date_pattern3 = r'(\d{1,2})[/\-\.](\d{1,2})[/\-\.](\d{4})'
    
    # Dictionary to convert month names to numbers
    month_dict = {
        'january': '01', 'february': '02', 'march': '03', 'april': '04',
        'may': '05', 'june': '06', 'july': '07', 'august': '08',
        'september': '09', 'october': '10', 'november': '11', 'december': '12'
    }
    
    for line in lines:
        # Extract the timestamp from the line
        timestamp_match = re.match(r'\[(\d{2}:\d{2}:\d{2})\]\s*(.*)', line)
        if timestamp_match:
            timestamp = timestamp_match.group(1)
            text = timestamp_match.group(2)
            
            # Find dates in the text
            dates_found = []
            
            # Look for dates in format "18th of March 2020"
            for match in re.finditer(date_pattern1, text, re.IGNORECASE):
                day = match.group(1).zfill(2)
                month = month_dict.get(match.group(2).lower(), '00')
                year = match.group(3)
                if month != '00':  # Only add if month is valid
                    dates_found.append(f"{day}/{month}/{year}")
            
            # Look for dates in format "March 18, 2020"
            for match in re.finditer(date_pattern2, text, re.IGNORECASE):
                month = month_dict.get(match.group(1).lower(), '00')
                day = match.group(2).zfill(2)
                year = match.group(3)
                if month != '00':  # Only add if month is valid
                    dates_found.append(f"{day}/{month}/{year}")
            
            # Look for dates in format "18/03/2020"
            for match in re.finditer(date_pattern3, text):
                day = match.group(1).zfill(2)
                month = match.group(2).zfill(2)
                year = match.group(3)
                dates_found.append(f"{day}/{month}/{year}")
            
            # Add data to lists
            for date in dates_found:
                entry_timestamps.append(timestamp)
                extracted_dates.append(date)
                extracted_texts.append(text)
    
    # Create a DataFrame
    data = {
        'Entry Timestamp': entry_timestamps,
        'Extracted Date': extracted_dates,
        'Original Text': extracted_texts
    }
    df = pd.DataFrame(data)
    
    # Save to Excel
    df.to_excel(output_file, index=False)
    print(f"Extracted {len(extracted_dates)} dates to {output_file}")

if __name__ == "__main__":
    extract_dates_times()
