#SPIDER WEBSCARPER
#DEVELOPED BY: Orangeman9590

# imports
import re
import requests
import requests.exceptions
from urllib.parse import urlsplit
from collections import deque
from bs4 import BeautifulSoup
import termcolor
from termcolor import colored
import os
import time



spider = '''
  ___________________.___________  _____________________ 
 /   _____/\______   \   \______ \ \_   _____/\______   \    |  |  
 \_____  \  |     ___/   ||    |  \ |    __)_  |       _/    \()/ 
 /        \ |    |   |   ||    `   \|        \ |    |   \   /(__)\ 
/_______  / |____|   |___/_______  /_______  / |____|_  /   |    |
        \/                       \/        \/         \/
{+}---------------{Developed By: Orangeman}--------------------{+}
'''


# Main Loop
done = False
while done == False:
    os.system('clear')
    print(colored(spider, 'cyan'))
    print(colored('ENTER THE URL YOU WANT TO SCRAPE(FULL URL)', 'red'))
    starting_url = input('spider> ')
    unprocessed_urls = deque([starting_url])
    processed_urls = set()
    emails = set()
    r = requests.get(starting_url)
    status = r.status_code
    os.system('clear')
    # Check if connected
    if status == 200:
        print(colored('CONNECTED SUCCESSFULLY.', 'red'))
        # Searches for emails
        while len(unprocessed_urls):

            url = unprocessed_urls.popleft()
            processed_urls.add(url)

            parts = urlsplit(url)
            base_url = "{0.scheme}://{0.netloc}".format(parts)
            path = url[:url.rfind('/')+1] if '/' in parts.path else url

            print("CRAWLING URL %s" % url)
            try:
                response = requests.get(url)
            except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
                continue

            new_emails = set(re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", response.text, re.I))
            emails.update(new_emails)
            print(emails)
            soup = BeautifulSoup(response.text, 'lxml')
            for anchor in soup.find_all("a"):
                
                link = anchor.attrs["href"] if "href" in anchor.attrs else ''
                if link.startswith('/'):
                    link = base_url + link
                elif not link.startswith('http'):
                    link = path + link
                if not link in unprocessed_urls and not link in processed_urls:
                    unprocessed_urls.append(link)
                if quit():
                    print(colored('WOULD YOU LIKE SAVE ALL THE EMAILS GATHERED IN A FILE?[Y/N]', 'cyan'))
                    validate = input('spider> ')
                    if validate == 'Y' :
                        f = open('emails.txt', 'w+')
                        for email in emails :
                            f.write(email + '\n')
                            done = True
                        print(colored('SAVED IN FILE: emails.txt IN THE SAME DIRECTORY AS PROGRAM'))
                    elif validate == 'N' :
                        print(colored('EXITING'))
                        quit()
        # File Gather
        print(colored('WOULD YOU LIKE SAVE ALL THE EMAILS GATHERED IN A FILE?[Y/N]', 'cyan'))
        validate = input('spider> ')
        if validate == 'Y':
            f = open('emails.txt', 'w+')
            for email in emails:
                f.write(email + '\n')
                done = True
            print(colored('SAVED IN FILE: emails.txt IN THE SAME DIRECTORY AS PROGRAM'))
        elif validate == 'N':
            print(colored('EXITING'))
            quit()




    else:
        print(colored('CONNECTION UNSUCCESSFULL.'))
        time.sleep(2)
