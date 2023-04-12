import requests

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

with open(file_path, "r", encoding="utf-8") as file, open("valid_urls.txt", "w") as valid_file:
    for line in file:
        url = line.strip()

        if not url:  
            continue

        with requests.Session() as session:
            response = session.get(url, allow_redirects=True, timeout=5)
            redirects = response.history[:3]  
            num_redirects = len(redirects)

        if redirects:
            final_url = response.url
            valid_urls.append(url)
            print(f"The URL {url} redirected {num_redirects} times to {final_url}")
            valid_file.write(f"{url}\n")
        else:
            print(f"The URL {url} did not redirect")

print(f"Valid URLs saved to valid_urls.txt")
