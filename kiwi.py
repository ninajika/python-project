import regex
from cloudscraper import create_scraper

class Qiwi:
    def __init__(self, url) -> None:
        self.url = url

    @staticmethod
    def decrypt_token_and_file_name(content):
        script_pattern = regex.compile(r'<script\b[^>]*>(.*?)</script', regex.DOTALL)
        slug_pattern = regex.compile(r'"slug"\s*:\s*"([^"]+)"')
        file_extension_pattern = regex.compile(r'"fileExtension"\s*:\s*"([^"]+)"')

        for script_match in script_pattern.finditer(content):
            script_content = script_match.group(1)
            cleaned_script_content = script_content.replace('\\"', '"').replace('\\n', '').replace('\\t', '').strip()
            slug_match = slug_pattern.search(cleaned_script_content)
            file_extension_match = file_extension_pattern.search(cleaned_script_content)

            if slug_match and file_extension_match:
                slug = slug_match.group(1)
                file_extension = file_extension_match.group(1)
                file_name = f"{slug}.{file_extension}"

                return file_name

        return None

    def generate_link(self):
        try:
            with create_scraper() as session:
                res = session.get(self.url, verify=True)
                filename = self.decrypt_token_and_file_name(res.text)
                if filename is not None:
                    return "https://qiwi.lol/" + filename
                else:
                    return "broken link"
        except Exception as e:
            print(e)

    
d = Qiwi().generate_link()
print("Generate Link", d)
