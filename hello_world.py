# hello_world.py
import sys
import requests
import json
from datetime import datetime
import re

class HelloWorldOSINT:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (compatible; HelloWorld-OSINT/1.0)"
        }

    def validate_phone(self, phone: str):
        phone = re.sub(r'\D', '', phone)
        if len(phone) < 10:
            return {"status": "invalid", "message": "Phone number too short"}
        return {"status": "valid", "formatted": f"+{phone}" if not phone.startswith('+') else phone}

    def numverify_lookup(self, phone: str, api_key: str = None):
        try:
            url = f"http://apilayer.net/api/validate?access_key={api_key}&number={phone}"
            r = requests.get(url, headers=self.headers, timeout=10)
            return r.json() if r.ok else None
        except:
            return None

    def check_breaches(self, email_or_phone: str):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Checking breaches for {email_or_phone}...")
        return {
            "found": "Unknown - Use https://haveibeenpwned.com",
            "recommendation": "Check manually on HaveIBeenPwned.com"
        }

    def google_dorks(self, phone: str):
        dorks = [
            f'"{phone}"',
            f'"{phone}" site:facebook.com',
            f'"{phone}" site:instagram.com',
            f'"{phone}" filetype:pdf',
            f'"{phone}" "gmail" OR "email"',
        ]
        print("\n🔍 Useful Google Dorks:")
        for d in dorks:
            print(f"   https://google.com/search?q={requests.utils.quote(d)}")

    def run(self, phone: str, api_key: str = None):
        print("="*60)
        print("🔍 Hello World OSINT Tool")
        print("="*60)

        info = self.validate_phone(phone)
        print(f"📱 Phone      : {phone}")
        print(f"Status        : {info.get('status')}")

        if info.get('status') == 'valid':
            print("\n🌐 Running OSINT modules...")

            carrier_info = self.numverify_lookup(info['formatted'], api_key)
            if carrier_info and carrier_info.get('valid'):
                print(f"Carrier       : {carrier_info.get('carrier')}")
                print(f"Location      : {carrier_info.get('location')} ({carrier_info.get('country_name')})")
                print(f"Line Type     : {carrier_info.get('line_type')}")

            self.check_breaches(phone)
            self.google_dorks(phone)

            print("\n💡 Tip: For better results, also search the number on:")
            print("   • Truecaller, Whitepages, FastPeopleSearch")
            print("   • Social media platforms directly")

        print("="*60)
        print("⚖️  Use only for lawful purposes with consent.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python hello_world.py <phone_number> [numverify_api_key]")
        print("Example: python hello_world.py +919876543210")
        sys.exit(1)

    tool = HelloWorldOSINT()
    tool.run(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
