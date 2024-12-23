from itertools import zip_longest
from model import NotamEntry, session
import re
import PyPDF2


from datetime import datetime

def extract_text_from_pdf(pdf_path):
    """
    Extract text from a PDF file using PyPDF2.
    """
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text()
        return text

def convert_date_format(date_str):
    """
    Convert various date formats to standard SQL format: YYYY-MM-DD HH:MM:SS.
    """
    date_str_numeric = re.sub(r'[^\d]', '', date_str)

    if len(date_str_numeric) == 12:
        year_prefix = '20'
        year = date_str_numeric[:2]
        month = date_str_numeric[2:4]
        day = date_str_numeric[4:6]
        hour = date_str_numeric[6:8]
        minute = date_str_numeric[8:10]
        date_str = f"{day}-{month}-{year_prefix}{year} {hour}:{minute}"
    elif len(date_str_numeric) == 10:
        year_prefix = '20'
        year = date_str_numeric[:2]
        month = date_str_numeric[2:4]
        day = date_str_numeric[4:6]
        hour = date_str_numeric[6:8]
        minute = date_str_numeric[8:10]
        date_str = f"{day}-{month}-{year_prefix}{year} {hour}:{minute}"
    else:
        return None

    try:
        datetime_obj = datetime.strptime(date_str, '%d-%m-%Y %H:%M')
        return datetime_obj.strftime('%Y-%m-%d %H:%M:%S')
    except ValueError:
        return None


def extract_notam_entries(text):
    notam_pattern = r'([A-Z]\d{4}/\d{2} NOTAM([A-Z]R?)(?:.*?)(?=Q\)|SOURCE:))'
    between_q_a_pattern = r'Q\)\s*(.*?)\s*A\)'
    between_b_c_pattern = r'B\)\s*(.*?)\s*C\)'
    between_c_d_or_e_pattern = r'C\)\s*(.*?)\s*(?:D\)|E\))'
    e_source_pattern = r'E\)\s*(.*?)\s*(?=F\)|G\)|CREATED:)'
    between_g_created_pattern = r'G\)\s*(\S)\s*CREATED\)'
    created_pattern = r'CREATED:\s*(.*?)\s*(?=SOURCE:)'
    source_pattern = r'SOURCE:\s*(.*?)\s*$'
    default_value = None
    
    notam_number_data = []
    first_part_list = []
    a_b_data = []
    b_c_data = []
    c_d_data = []
    text_data = []
    e_f_data = []
    fg_data = []
    g_data = []
    createddata = []
    sourcedata = []
   
    
    notam_matches = re.finditer(notam_pattern, text, re.MULTILINE | re.DOTALL)
    # series, number, type , additional data
    for match in notam_matches:
        notam_text = match.group(0)
        notam_number_pattern = r'([A-Z])(\d{4}/\d{2})\s*NOTAM([A-Z]R?)'
        notam_number_match = re.search(notam_number_pattern, notam_text)
        if notam_number_match:
            first_alphabet = notam_number_match.group(1) if notam_number_match.group(1) else 'null'
            # print(first_alphabet)  # Print first_alphabet or 'null'
            number_after_alphabet = notam_number_match.group(2)
            last_letter = notam_number_match.group(3)
            after_last_letter = notam_text.split(last_letter)[-1]
            additional_data = re.split(r'\s*Q\)', after_last_letter, maxsplit=1)[0].strip()
            notam_number_data.append((first_alphabet,number_after_alphabet,last_letter,additional_data[:50]))
    
        
    # Q to A data  (fir1 2 3, qualifier1 2 3, traffic1 2, purpose1 2 3, scope 1 2, from FL, upto FL, center lat, center lon, radius)
    q_a_matches = re.finditer(between_q_a_pattern, text, re.MULTILINE | re.DOTALL)
    for match in q_a_matches:
        between_q_a_data = match.group(1).strip()
        parts = between_q_a_data.split("/")
        first_part = parts[0]
        second_part = parts[1] if len(parts) > 1 else ""
        third_part = parts[2] if len(parts) > 2 else ""
        fourth_part = parts[3] if len(parts) > 3 else ""
        fifth_part = parts[4] if len(parts) > 4 else ""
        sixth_part = parts[5] if len(parts) > 5 else ""
        seventh_part = parts[6] if len(parts) > 6 else ""
        eighth_part = parts[7] if len(parts) > 7 else ""
        center_lat1 = center_lon1 = radius = None
        if eighth_part:
            lat_lon_radius_pattern = r'(\d{4})(N)(\d{5})(E)(\d{3})'
            lat_lon_radius_match = re.search(lat_lon_radius_pattern, eighth_part)
            if lat_lon_radius_match:
                center_lat1 = lat_lon_radius_match.group(1) + lat_lon_radius_match.group(2)
                center_lon1 = lat_lon_radius_match.group(3) + lat_lon_radius_match.group(4)
                radius = lat_lon_radius_match.group(5)
            else:
                print("No match found for lat, lon, or radius.")
        first_part_list.append((first_part, second_part, third_part, fourth_part, fifth_part, sixth_part, seventh_part, center_lat1, center_lon1, radius))
    
    # airport fir1, fir2, fir3 data
    between_a_b_pattern = r'A\)\s*([^()]*?)\s*B\)'
    a_b_matches = re.finditer(between_a_b_pattern, text, re.MULTILINE | re.DOTALL)

    for match in a_b_matches:
     between_a_b_data = match.group(1).strip()
    
    # Split the data into individual entries
     fir_data = [entry.strip() for entry in between_a_b_data.split(',') if len(entry.strip()) > 1]
     airport_fir1 = fir_data[0].strip() if len(fir_data) > 0 else ''
     airport_fir2 = fir_data[1].strip() if len(fir_data) > 1 else ''
     airport_fir3 = fir_data[2].strip() if len(fir_data) > 2 else ''
     airport_fir4 = fir_data[3].strip() if len(fir_data) > 3 else ''
    
    # Append the results
     a_b_data.append((airport_fir1, airport_fir2, airport_fir3, airport_fir4))


        
    # b to c data (start date)
    b_c_matches = re.finditer(between_b_c_pattern, text, re.MULTILINE | re.DOTALL)
    
    for match in b_c_matches:
        
        between_b_c_data = match.group(1).strip()
        print(between_b_c_data)
        if not between_b_c_data and not re.search(r'\([A-Z]+\)', between_b_c_data):
            b_c_data.append("")
        else:
            formatted_start_date = convert_date_format(between_b_c_data)
            if formatted_start_date:
                b_c_data.append(formatted_start_date)
            else:
                b_c_data.append(between_b_c_data)
    
    # c to d or e (end date)
    between_c_d_or_e_matches = re.finditer(between_c_d_or_e_pattern, text, re.MULTILINE | re.DOTALL)
    for match in between_c_d_or_e_matches:
        between_c_d_or_e_data = match.group(1).strip()
        if not re.search(r'\([A-Z]+\)', between_c_d_or_e_data):
            formatted_end_date = convert_date_format(between_c_d_or_e_data)
            if formatted_end_date:
                end_date = formatted_end_date
                c_d_data.append(end_date)
            else:
                c_d_data.append(between_c_d_or_e_data)
        else:
            c_d_data.append("[Blank]")
            
    # D to E data (day time)
    patterns = r'([A-Z]\d{4}/\d{2} NOTAM[A-Z]R?.*?Q\).*?SOURCE:.*?)(?=\s*[A-Z]\d{4}/\d{2} NOTAM|$)'
    matche = re.findall(patterns, text, re.MULTILINE | re.DOTALL)
    for notam in matche:
        entries = re.findall(r'D\)\s*(.*?)\s*E\)', notam, re.DOTALL)
        if not entries:
            e_f_data.append("null")
        else:
            for entry in entries:
                e_f_data.append(entry.strip())
                
    until_date_pattern = r'UNTIL\s(\d{2}\s\w{3}\s\d{4}\s\d{2}:\d{2}\s\d{4})'

# List to store extracted data
    text_data = []

# Process the NOTAM text
    e_source_matches = re.finditer(e_source_pattern, text, re.MULTILINE | re.DOTALL)
    for match in e_source_matches:
        e_source_data = match.group(1).strip()
        text_data.append(e_source_data)

    # Extract UNTIL date from the current match
        until_match = re.search(until_date_pattern, e_source_data)
        if until_match:
            until_date = until_match.group(1)
            print(f"UNTIL Date: {until_date}")
        else:
            print("UNTIL Date: Not Found")

    # Print the description data
        print(f"Description: {e_source_data}")
        print("-" * 50)

# Output the collected descriptions
        print("\nCollected Text Data:", text_data)
       
    
    # F to G/ created on data (lower limit)
    notam_patterns = r'([A-Z]\d{4}/\d{2} NOTAM[A-Z]R?.*?Q\).*?SOURCE:.*?)(?=\s*[A-Z]\d{4}/\d{2} NOTAM|$)'
    notam_matche = re.findall(notam_patterns, text, re.MULTILINE | re.DOTALL)

   # Loop over each NOTAM to find data between F) and G) or F) and CREATED
    for notam in notam_matche:
    # First, try to find single character data between F) and G)
     f_to_g = re.findall(r'F\)\s*(\S)\s*G\)', notam, re.DOTALL)
     if f_to_g:
        # If data between F) and G) is found, add it
        for entry in f_to_g:
            fg_data.append(entry.strip())
     else:
        # If no G), try to find single character data between F) and CREATED
        f_to_created = re.findall(r'F\)\s*(\S)\s*CREATED', notam, re.DOTALL)
        if f_to_created:
            # If data between F) and CREATED is found, add it
            for entry in f_to_created:
                fg_data.append(entry.strip())
        else:
            # If neither G) nor CREATED are found, append null
            fg_data.append("null")
            
    
    # g to reated data (upper limit)
    upper_match = re.findall(notam_patterns, text, re.MULTILINE | re.DOTALL)
   # Loop over each NOTAM to find data between F) and G) or F) and CREATED
    for notam in upper_match:
    # First, try to find single character data between F) and G)
     g_to_craeted = re.findall(between_g_created_pattern, notam, re.DOTALL)
     if g_to_craeted:
        # If data between F) and G) is found, add it
        for entry in g_to_craeted:
            g_data.append(entry.strip())
     else:
            g_data.append("null")
            
    #craeted data
    created_matches = re.finditer(created_pattern, text, re.MULTILINE | re.DOTALL)
    text_description = None  # Initialize default text description
    for match in created_matches:
     created_data = match.group(1).strip()
     created = created_data
     createddata.append(created)

    # Source Data
    source_match = re.finditer(source_pattern, text, re.MULTILINE | re.DOTALL)
    for match in source_match:
     source_data = match.group(1).strip() if match and match.group(1).strip() else "null"
     sourcedata.append(source_data)
     
    # notam_data_pattern = r'([A-Z]\d{4}/\d{2} NOTAM[A-Z]? [A-Z]\d{4}/\d{2}[\s\S]*?SOURCE:.*?)\s*$'
    notam_data_pattern = r'([A-Z]\d{4}/\d{2}\s*NOTAM[A-Z]?\s*.*?CREATED:.*?)(?=\s*$)'

    notam_data =[] 
    notam_ma = re.finditer(notam_data_pattern,text, re.MULTILINE | re.DOTALL)
    # series, number, type , additional data
    for match in notam_ma:
        notam_text = match.group(0)
        notam_data.append((notam_text))
        # print(notam_data)
    all_notam_entries = []
    if len(notam_number_data) != len(first_part_list):
     print(f"Mismatch: notam_number_data has {len(notam_number_data)} items, first_part_list has {len(first_part_list)} items.")
    # print("First Part List:", first_part_list)
    for notam_number_datas, part, a_b_datas, b_c_datas, c_d_datas, e_f_datas, g_datas, f_g_datas, text_description, created, source, text in zip_longest(
        notam_number_data, first_part_list, a_b_data, b_c_data, c_d_data, e_f_data, g_data, fg_data, text_data, createddata, sourcedata, notam_data, fillvalue=default_value):
    
    # Skip iteration if all data fields are None or empty
     if all(value in (None, '', []) for value in [notam_number_datas, part, a_b_datas, b_c_datas, c_d_datas, e_f_datas, g_datas, f_g_datas, text_description, created, source, text]):
        continue

    # Safely handle notam_number_datas and part
     series = notam_number_datas[0] if notam_number_datas and len(notam_number_datas) > 0 else ''
     number = notam_number_datas[1] if notam_number_datas and len(notam_number_datas) > 1 else ''
     notam_type = notam_number_datas[2] if notam_number_datas and len(notam_number_datas) > 2 else ''
     additional_info = notam_number_datas[3] if notam_number_datas and len(notam_number_datas) > 3 else ''
     fir = part[0] if part and len(part) > 0 else ''
     qualifier = part[1][0] if part and len(part) > 1 and len(part[1]) > 0 else ''
     qualifier1 = part[1][1:3] if part and len(part[1]) > 2 else ''
     qualifier2 = part[1][3:5] if part and len(part[1]) > 4 else ''
     traffic = part[2] if part and len(part) > 2 else ''
     purpose = part[3] if part and len(part) > 3 else ''
     scope = part[4] if part and len(part) > 4 else ''
     from_fl = part[5] if part and len(part) > 5 else None
     upto_fl = part[6] if part and len(part) > 6 else None
     center_lat = part[7] if part and len(part) > 7 else None
     center_lon = part[8] if part and len(part) > 8 else None
     radius_of_area_affected = part[9] if part and len(part) > 9 else None

    # Create the NotamEntry object
     notam_entry = NotamEntry(
        series=series,
        number=number,
        type=notam_type,
        additional_info=additional_info,
        fir=fir,
        qualifier=qualifier,
        qualifier1=qualifier1,
        qualifier2=qualifier2,
        traffic=traffic,
        purpose=purpose,
        scope=scope,
        from_fl=from_fl,
        upto_fl=upto_fl,
        center_lat=center_lat,
        center_lon=center_lon,
        radius_of_area_affected=radius_of_area_affected,
        airport_fir=a_b_datas[0] if a_b_datas and len(a_b_datas) > 0 else '',
        start_date=b_c_datas if b_c_datas else '',
        end_date=c_d_datas if c_d_datas else '',
        day_time=e_f_datas if e_f_datas else '',
        upper_limit=g_datas if g_datas else '',
        lower_limit=f_g_datas if f_g_datas else '',
        text_description=text_description,
        created_on=datetime.now(),
        source=source,
        notam=text
    )

     all_notam_entries.append(notam_entry)

# Add all entries to the session and commit after the loop
    if all_notam_entries:  # Only commit if there are entries to add
     session.add_all(all_notam_entries)
     session.commit()

  

def main():
    pdf_path = r"C:\Users\LENOVO\Desktop\ANS_Register_Extraction\NOTAM\NOTAM_India_Sample_08Sept24_CNPL.pdf"
    pdf_text = extract_text_from_pdf(pdf_path)
    extract_notam_entries(pdf_text)

if __name__ == "__main__":
    main()
