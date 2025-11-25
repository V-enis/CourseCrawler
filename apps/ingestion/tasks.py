import os
import subprocess
from celery import shared_task

@shared_task
def run_mit_ocw_scraper():
    """
    A Celery task to run the MIT OCW Scrapy spider.
    """
    scrapy_project_path = '/code/cc_scrapers'
    spider_name = 'mit'

    print(f"Celery task started: Running spider '{spider_name}'...")

    try:
        result = subprocess.run(
            ['scrapy', 'crawl', spider_name],
            cwd=scrapy_project_path, # like running 'cd'
            capture_output=True,
            text=True,
            check=True # raise an exception if scrapy returns nonzero exit code
        )
        print(f"Scrapy stdout:\n{result.stdout}")
        return f"Spider '{spider_name}' completed successfully."
    except FileNotFoundError:
        error_message = "Error: 'scrapy' command not found. Is Scrapy installed in the container?"
        print(error_message)
        return error_message
    except subprocess.CalledProcessError as e:
        # standard error from scrapy upon failure. 
        error_message = f"Spider '{spider_name}' failed with exit code {e.returncode}.\nStderr:\n{e.stderr}"
        print(error_message)
        return error_message
    except Exception as e:
        error_message = f"An unexpected error occurred: {e}"
        print(error_message)
        return error_message