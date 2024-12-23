import requests
import hashlib
import hmac
import base64
import time
 
from datetime import datetime, timedelta
from notam_entry import extract_notam_entries
 
class NotamService:
    def __init__(self, api_key, api_secret, base_url):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = base_url
    def is_notam_recent(self,notam_issuetime_str):
        issuetime = datetime.strptime(notam_issuetime_str, '%Y-%m-%dT%H:%M:%SZ')
    # Get the current UTC time
        current_time = datetime.utcnow()
    # Calculate the time difference
        time_difference = current_time - issuetime
    # Check if the time difference is 15 minutes or less
        return time_difference <= timedelta(minutes=3000)
 
    def get_iso_timestamp(self):
        """Returns the current ISO timestamp with Z notation."""
        current_date = datetime.utcnow()
        return current_date.isoformat(timespec='seconds') + 'Z'
 
    def get_notam_data(self,airport):
        """Fetch NOTAM data for the specified region."""
        endpoint = f"{self.api_key}/reports/notam/station/{airport}.json?"
 
        # Sign the request URL
        signed_url = self.sign_request(f"{self.base_url}{endpoint}")
        print(f"Signed URL: {signed_url}")
        try:
            response = requests.get(signed_url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as error:
            print(f"Error fetching NOTAM data: {error}")
            raise error
 
    def sign_request(self, url):
        """Generates a signed URL using HMAC-SHA1."""
        timestamp = str(int(time.time()))  # POSIX timestamp in seconds
        string_to_sign = f"{self.api_key}:{timestamp}"
 
        # HMAC-SHA1 signing and Base64 encoding
        hmac_digest = hmac.new(
            self.api_secret.encode('utf-8'),
            string_to_sign.encode('utf-8'),
            hashlib.sha1
        ).digest()
        base64_signature = base64.b64encode(hmac_digest).decode('utf-8')
 
        # Replace special characters as required
        modified_signature = base64_signature.replace('/', '_').replace('+', '-')
 
        # Add signature and timestamp to the URL
        query_char = '&' if '?' in url else '?'
        return f"{url}{query_char}sig={modified_signature}&ts={timestamp}"
 
# Example usage
def lambda_handler(event, context):
 
    api_key = "GTt8Njnc3Z7P"
    api_secret = "JqbpMSopmwISsVBWvyEmywPEbePUoW6lkbxGH0h1Um"
    base_url = "http://api.velocityweather.com/v1/"
    icao_codes = [
    "VEGT",
    #   "VAAU", "VABB", "VABO", "VABP", "VABV", "VADN", "VAGD", "VAHS",
    # "VAID", "VAJB", "VAJJ", "VAJL", "VAKE", "VAKP", "VAKS", "VAMA", "VANP",
    # "VAOZ", "VAPO", "VAPR", "VASD", "VASU", "VAUD", "VEAH", "VEAT", "VEAY",
    # "VEBI", "VEBN", "VEBD", "VEBS", "VEBU", "VECC", "VECO", "VEDG", "VEGK",
    # "VEDO", "VEGT", "VEGY", "VEHO", "VEIM", "VEJR", "VEJS", "VEJH", "VEJT",
    # "VEKI", "VEKO", "VELP", "VELR", "VEMN", "VEMR", "VEPT", "VEPY", "VERC",
    # "VERK", "VERP", "VERU", "VETJ", "VIAG", "VIAR", "VIBR", "VIBY", "VICG",
    # "VIDD", "VIDN", "VIDP", "VIDX", "VIGG", "VIGR", "VIHR", "VIJO", "VIJP",
    # "VIJU", "VIKG", "VILD", "VILH", "VILK", "VIPG", "VIPT", "VISM", "VIUT",
    # "VOAT", "VOBG", "VOBL", "VOBM", "VOBR", "VOBZ", "VOCB", "VOCI", "VOCL",
    # "VOCP", "VOGA", "VOGB", "VOGO", "VOHB", "VOHS", "VOHY", "VOJV", "VOKN",
    # "VOKU", "VOMD", "VOML", "VOMM", "VOMY", "VOPB", "VOPC", "VOPN", "VORY",
    # "VOSM", "VOSH", "VOSR", "VOTK", "VOTP", "VOTR", "VOTV", "VOVZ"
]
    service = NotamService(api_key, api_secret, base_url)
    # Example coordinates
     # loop over icao code
    for code in icao_codes:    
        try:
            count=0
            notam_data = service.get_notam_data(code)
            text = ""
            notams = notam_data['notams']['data']['notams']
            print(f"notams {len(notams)}")
            for notam in notams:
                if service.is_notam_recent(notam['issuetime']):
                 print(notam['raw_text'])
                 extract_notam_entries(notam['raw_text'])
                 count+=1
            print(f"processed {count} notams for airport {code}")
 
        except Exception as e:
            print(f"Failed to fetch NOTAM data: {e}")
 
if __name__ == "__main__":
    lambda_handler(None, None)
 