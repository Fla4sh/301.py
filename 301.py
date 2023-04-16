import requests
from urllib.parse import urlparse
import threading

print('''\
                                                                                    
                                                                                    
██████╗  ██████╗  ██╗
╚════██╗██╔═████╗███║
 █████╔╝██║██╔██║╚██║
 ╚═══██╗████╔╝██║ ██║
██████╔╝╚██████╔╝ ██║
╚═════╝  ╚═════╝  ╚═╝
                     @github.com/Fla4sh
                     @twitter : fla4sh403\
''')

file_path = input("Please enter your file: ")

valid_urls = []

def check_url(url):
    if not url:
        return

    try:
        with requests.Session() as session:
            response = session.get(url, allow_redirects=True, timeout=5)
            redirects = response.history[:5]
            num_redirects = len(redirects)

        if redirects:
            final_url = response.url
            parsed_url = urlparse(url)
            parsed_final_url = urlparse(final_url)
            if parsed_url.netloc != parsed_final_url.netloc:  # check if domains are different
                valid_urls.append(url)
                print(f"The URL {url} redirected {num_redirects} times to {final_url}")
            else:
                print(f"The URL {url} redirected {num_redirects} times to the same domain ({parsed_url.netloc})")
        else:
            print(f"The URL {url} did not redirect")
    except Exception as e:
        print(f"Error occurred while checking URL: {url}")
        print(e)

with open(file_path, "r", encoding="utf-8") as file, open("valid_urls.txt", "w") as valid_file:
    threads = []
    for line in file:
        url = line.strip()
        t = threading.Thread(target=check_url, args=(url,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    valid_urls_to_write = [url for url in valid_urls if urlparse(url).netloc != urlparse(file_path).netloc and urlparse(url).netloc.endswith("." + urlparse(file_path).netloc)] # filter valid URLs that redirect to another domain or subdomain
    valid_file.write("\n".join(valid_urls_to_write))

print(f"Valid URLs saved to valid_urls.txt")
