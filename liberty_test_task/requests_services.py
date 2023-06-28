import requests

from liberty_test_task.logger import Logger
from liberty_test_task.settings import GET_COMMENTS_URL, GET_POSTS_URL


def fetch_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        Logger.info(
            "Error occurred during the request to the %s: - %s", url, e
        )
        raise requests.RequestException(
            f"Error occurred during the request to the {url}: - {e}"
        ) from e
    except Exception as e:
        Logger(
            "An unexpected error occurred during the request to the %s: - %s",
            url,
            e,
        )
        raise Exception(
            f"An unexpected error occurred during the request "
            f"to the {url}: - {e}"
        ) from e

    else:
        return response.json()


def fetch_posts():
    fetched_posts = fetch_data(GET_POSTS_URL)
    Logger.info("%s posts are fetched", len(fetched_posts))
    return fetched_posts


def fetch_comments():
    fetched_comments = fetch_data(GET_COMMENTS_URL)
    Logger.info("%s comments are fetched", len(fetched_comments))
    return fetched_comments
