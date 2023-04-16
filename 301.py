import requests
from concurrent.futures import ThreadPoolExecutor

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
    try:
        with requests.Session() as session:
            response = session.get(url, allow_redirects=True, timeout=5)
            redirects = response.history[:5]
            num_redirects = len(redirects)

        if redirects:
            final_url = response.url
            parsed_url = requests.utils.urlparse(url)
            parsed_final_url = requests.utils.urlparse(final_url)
            if parsed_url.netloc != parsed_final_url.netloc:
                valid_urls.append(url)
                print(f"The URL {url} redirected {num_redirects} times to {final_url}")
            else:
                print(f"The URL {url} redirected {num_redirects} times to the same domain ({parsed_url.netloc})")
        else:
            print(f"The URL {url} did not redirect")
    except Exception as e:
        print(f"Error occurred while checking URL: {url}")
        print(e)

with open(file_path, "r", encoding="utf-8") as file, open("valid_urls.txt", "w") as valid_file, ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(check_url, url.strip()) for url in file]
    for future in futures:
        future.result()

    valid_urls_to_write = [url for url in valid_urls if requests.utils.urlparse(url).netloc != requests.utils.urlparse(file_path).netloc and requests.utils.urlparse(url).netloc.endswith("." + requests.utils.urlparse(file_path).netloc)]
    valid_file.write("\n".join(valid_urls_to_write))

print(f"Valid URLs saved to valid_urls.txt")
