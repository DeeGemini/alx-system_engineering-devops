#!/usr/bin/python3
"""
This module provides a function to query the Reddit API and print the titles of the first 10 hot posts listed for a given subreddit.
"""

import requests

def top_ten(subreddit):
    """
    Prints the titles of the first 10 hot posts listed for a given subreddit.

    Args:
        subreddit (str): The name of the subreddit.

    Returns:
        None
    """
    # URL for the Reddit API endpoint to get hot posts
    url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit=10"

    # Set custom User-Agent header to avoid "Too Many Requests" error
    headers = {'User-Agent': 'MyBot/0.1'}

    # Send GET request to the API
    response = requests.get(url, headers=headers)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse JSON response
        data = response.json()
        # Extract titles of hot posts and print them
        for post in data['data']['children']:
            print(post['data']['title'])
    else:
        # If subreddit is invalid or request failed, print None
        print(None)

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Please pass an argument for the subreddit to search.")
    else:
        top_ten(sys.argv[1])

