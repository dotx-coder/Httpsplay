
# Httpsplay 

Httpsplay is a command-line tool for checking HTTP response codes of URLs, supporting both single URL and batch file processing. It uses asyncio and aiohttp for asynchronous URL checking, allowing efficient handling of multiple requests concurrently.

## Features

- **Asynchronous Processing:** Utilizes asyncio and aiohttp for concurrent HTTP requests.
- **Retry Mechanism:** Handles connection retries with customizable retry attempts.
- **HTTP Status Filtering:** Option to filter URLs based on specific HTTP status codes.
- **Logging:** Supports logging results to both console and file.
- **Customization:** Allows setting custom User-Agent and using HTTP proxies.

## Installation

Ensure you have Python 3.7+ installed. Clone the repository and install dependencies:

```bash
git clone https://github.com/your-repo-url.git
cd Sub0ut
pip install -r requirements.txt
```
## Usage
### Command-Line Arguments
```bash
python Sub0ut.py [-h] [-u URL] [-f FILE] [-r RETRIES] [-t TIMEOUT] [-o OUTPUT] [-c STATUS_CODE] [-v] [-a USER_AGENT] [-p PROXY]
```
**Function Usage:**
* **-d [Domain]**: The domain you want to enumerate subdomains of.
* **-o [Filename]**: Save the output into text file.
* **-v [Verbose]**: Enable verbose mode.
* **-p [Proxy_URL]**: Proxy URL to use for requests.
* **-a [User_Agent]**: Custom User-Agent header.
* **-r [Retries]**: Maximum number of retries (default: 3).
* **-t [Timeout]**: Timeout in seconds for requests (default: 10).
* 
## License

Httpsplay is licensed under the MIT license. take a look at the [LICENSE](https://GitHub.com/Httpsplay/main/LICENSE) for more information.>

## Credits
**Credit Goes To:**
* [the_lost_boy_231](https://github.com/the-lost-boy-231) -Programmer of this tool

## Thanks

* Special Thanks to [lostboy](https://Instagram.com/the_lost_boy_231) for his great work.

## Version
**Current version is 1.0**
