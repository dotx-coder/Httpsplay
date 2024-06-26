import argparse
import asyncio
import aiohttp
import logging
import sys
import traceback
from colorama import Fore, Style, init
from tabulate import tabulate
from http import HTTPStatus
import random
import os

init(autoreset=True)
os.system('clear')
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
    # Add more User-Agents as needed
]

def get_status_name(status_code):
    try:
        return HTTPStatus(status_code).phrase
    except ValueError:
        return "Unknown Status"

async def check_url(url, session, max_retries=3, timeout=10, log_file=None, filter_status=None, user_agent=None, proxy=None):
    retries = 0
    headers = {'User-Agent': user_agent or random.choice(USER_AGENTS)}
    while retries <= max_retries:
        try:
            logging.debug(f"Checking URL: {url}, Attempt: {retries + 1}")
            async with session.head(url, headers=headers, proxy=proxy, timeout=timeout) as response:
                status_code = response.status
                status_name = get_status_name(status_code)
                color = Fore.GREEN if 200 <= status_code < 300 else Fore.RED
                result = [url, f"{color}{status_code}{Style.RESET_ALL}", status_name]
                logging.debug(f"URL: {url}, Status Code: {status_code}, Status Name: {status_name}")
                if log_file:
                    logging.info(f"{url} - {status_code} - {status_name}")
                if filter_status is None or status_code == filter_status:
                    return result
                else:
                    return None
        except aiohttp.ClientError as e:
            if retries == max_retries:
                error_message = f"Failed after {max_retries} retries: {e}"
                logging.error(error_message)
                return [url, f"{Fore.RED}Failed after {max_retries} retries{Style.RESET_ALL}", "Failed"]
            retries += 1
            logging.debug(f"Retry {retries} for URL: {url} after ClientError: {e}")
            await asyncio.sleep(1)
        except asyncio.TimeoutError:
            if retries == max_retries:
                error_message = f"Timeout after {max_retries} retries"
                logging.error(error_message)
                return [url, f"{Fore.RED}Timeout after {max_retries} retries{Style.RESET_ALL}", "Timeout"]
            retries += 1
            logging.debug(f"Retry {retries} for URL: {url} after Timeout")
            await asyncio.sleep(1)
        except Exception as e:
            error_message = f"Unexpected error occurred: {e}"
            logging.error(error_message)
            logging.error(traceback.format_exc())
            return [url, f"{Fore.RED}Unexpected error{Style.RESET_ALL}", "Error"]

async def check_urls(urls, max_retries=3, timeout=10, output_file=None, filter_status=None, verbose=False, user_agent=None, proxy=None):
    results = []
    tasks = []

    # Configure logging to file
    logging.basicConfig(format="%(message)s", level=logging.INFO, filename=output_file, filemode='w')

    # Configure logging to console
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(logging.Formatter("%(message)s"))
    console_handler.setLevel(logging.DEBUG if verbose else logging.INFO)
    logging.getLogger("").addHandler(console_handler)
    logging.getLogger().setLevel(logging.DEBUG if verbose else logging.INFO)

    # Print banner
    print_banner("httpsplay")

    async with aiohttp.ClientSession() as session:
        for url in urls:
            url = url.strip()
            if not url.startswith(('http://', 'https://')):
                url = 'http://' + url  # Default to http if no scheme is provided
            tasks.append(check_url(url, session, max_retries, timeout, output_file, filter_status, user_agent, proxy))
        
        filtered_results = await asyncio.gather(*tasks)
        
        for result in filtered_results:
            if result is not None:
                results.append(result)
        
        print(tabulate(results, headers=["URL", "Status Code", "Status Name"], tablefmt="grid"))

def print_banner(text):
    # Print a colorful banner with the provided text
    banner_text = f"\n{Fore.CYAN} _     _   _                   _ {Style.RESET_ALL}"
    banner_text += f"\n{Fore.CYAN}█ █__ █ █_█ █_ _ __  ___ _ __ | █ __ _ _   _ {Style.RESET_ALL}"
    banner_text += f"\n{Fore.GREEN}█ '_ \█ __█ __█ '_ \/ __█ '_ \| █/ _` █ █ █ █ {Style.RESET_ALL}"
    banner_text += f"\n{Fore.RED}█ █ █ █ █_█ █_█ █_) \__ \ █_) | █ (_█ █ █_█ █ {Style.RESET_ALL}"
    banner_text += f"\n{Fore.GREEN}█_█ █_█\__█\__█ .__/█___/ .__/|_█\__,_█\__, █ {Style.RESET_ALL}"
    banner_text += f"\n{Fore.CYAN}              █_█       █_█            █___/ {Style.RESET_ALL}"
    print(banner_text)

def main():
    parser = argparse.ArgumentParser(description='Check HTTP response codes of URLs from a file or a single URL.')
    parser.add_argument('-u', '--url', help='A single URL to check.')
    parser.add_argument('-f', '--file', help='Path to the file containing URLs.')
    parser.add_argument('-r', '--retries', type=int, default=3, help='Maximum number of retries (default: 3).')
    parser.add_argument('-t', '--timeout', type=int, default=10, help='Timeout in seconds for requests (default: 10).')
    parser.add_argument('-o', '--output', help='Path to file for saving results.')
    parser.add_argument('-c', '--status-code', type=int, help='Filter URLs by HTTP status code.')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose mode.')
    parser.add_argument('-a', '--user-agent', help='Custom User-Agent header.')
    parser.add_argument('-p', '--proxy', help='Proxy URL to use for requests.')
    args = parser.parse_args()

    if not (args.url or args.file):
        parser.error('Either --url or --file must be specified.')

    if args.url:
        urls = [args.url]
    else:
        with open(args.file, 'r') as file:
            urls = file.readlines()

    asyncio.run(check_urls(urls, args.retries, args.timeout, args.output, args.status_code, args.verbose, args.user_agent, args.proxy))

if __name__ == '__main__':
    print_banner("httpsplay")
    main()
