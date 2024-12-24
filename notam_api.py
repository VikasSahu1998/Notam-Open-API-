import requests
from notam_entry import extract_notam_entries
# Define the API endpoint and API key
api_endpoint = "https://applications.icao.int/dataservices/api/notams-realtime-list"
# api_key = "0e933f98-5067-4062-bab7-059b4ec17605"
api_key = "a497e5c5-271c-443e-982e-99211f2cddb4"
# api_key = "32f59443-8ae8-4f2d-a6bf-80679c876091"
# api_endpoint = "https://dummyjson.com/c/9609-4fc7-44f1-bac0"
# api_key = "fb145f7c-3e3e-418d-b20a-9d84d190c8f5"
# List of ICAO codes
icao_codes = [
    "VAAH", "VAAU", "VABB", "VABO", "VABP", "VABV", "VADN", "VAGD", "VAHS",
    "VAID", "VAJB", "VAJJ", "VAJL", "VAKE", "VAKP", "VAKS", "VAMA", "VANP",
    "VAOZ", "VAPO", "VAPR", "VASD", "VASU", "VAUD", "VEAH", "VEAT", "VEAY",
    "VEBI", "VEBN", "VEBD", "VEBS", "VEBU", "VECC", "VECO", "VEDG", "VEGK",
    "VEDO", "VEGT", "VEGY", "VEHO", "VEIM", "VEJR", "VEJS", "VEJH", "VEJT",
    "VEKI", "VEKO", "VELP", "VELR", "VEMN", "VEMR", "VEPT", "VEPY", "VERC",
    "VERK", "VERP", "VERU", "VETJ", "VIAG", "VIAR", "VIBR", "VIBY", "VICG",
    "VIDD", "VIDN", "VIDP", "VIDX", "VIGG", "VIGR", "VIHR", "VIJO", "VIJP",
    "VIJU", "VIKG", "VILD", "VILH", "VILK", "VIPG", "VIPT", "VISM", "VIUT",
    "VOAT", "VOBG", "VOBL", "VOBM", "VOBR", "VOBZ", "VOCB", "VOCI", "VOCL",
    "VOCP", "VOGA", "VOGB", "VOGO", "VOHB", "VOHS", "VOHY", "VOJV", "VOKN",
    "VOKU", "VOMD", "VOML", "VOMM", "VOMY", "VOPB", "VOPC", "VOPN", "VORY",
    "VOSM", "VOSH", "VOSR", "VOTK", "VOTP", "VOTR", "VOTV", "VOVZ"
]

# Split the ICAO codes into chunks of 50 (adjust if needed)
chunk_size = 15
icao_chunks = [icao_codes[i:i + chunk_size] for i in range(0, len(icao_codes), chunk_size)]

# Function to call the API
def fetch_notam_data(icao_chunk):
    locations_param = ",".join(icao_chunk)
    params = {
        "api_key": api_key,
        "format": "jsoncsv",
        "criticality": "",
        "locations": locations_param
    }
    try:
        response = requests.get(api_endpoint, params=params)
        # response = requests.get(api_endpoint)  # Adjust to include necessary params if required
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred for chunk {icao_chunk}: {e}")
        return None

# Fetch and process data for each chunk
all_data = []
for chunk in icao_chunks:
    print(f"Fetching data for ICAO chunk: {chunk}")
    data = fetch_notam_data(chunk)
    if data:
        # Extract only the "all" field from each NOTAM
        extracted_data = [item["all"] for item in data if "all" in item]
        all_data.extend(extracted_data)

# Process or save the extracted data
print("Extracted 'all' fields:")
for item in all_data:
    print("Processing item:", item)
    extract_notam_entries(item)

print("Total NOTAM 'all' fields fetched:", len(all_data))



# from model import Base, engine
 
# Base.metadata.create_all(engine)
 
# exit()
 