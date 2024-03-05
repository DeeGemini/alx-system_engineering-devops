#!/usr/bin/python3
"""
This module provides a recursive function to query the Reddit API and return a list containing the titles of all hot articles for a given subreddit.
"""

import requests

def recurse(subreddit, hot_list=None, after=None):
    """
    Recursively queries the Reddit API and returns a list containing the titles of all hot articles for a given subreddit.

    Args:
        subreddit (str): The name of the subreddit.
        hot_list (list): A list to store the titles of hot articles. Defaults to None.
        after (str): The ID of the last post in the previous page. Used for pagination. Defaults to None.

    Returns:
        list or None: A list containing the titles of all hot articles for the given subreddit, or None if no results are found.
    """
    if hot_list is None:
        hot_list = []

    # URL for the Reddit API endpoint to get hot posts
    url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit=100"
    
    # If there's a pagination token, add it to the URL
    if after:
        url += f"&after={after}"

    # Set custom User-Agent header to avoid "Too Many Requests" error
    headers = {'User-Agent': 'MyBot/0.1'}

    # Send GET request to the API
    response = requests.get(url, headers=headers)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse JSON response
        data = response.json()
        
        # Extract titles of hot posts
        posts = data['data']['children']
        for post in posts:
            hot_list.append(post['data']['title'])

        # Get the ID of the last post in the current page for pagination
        after = data['data']['after']

        # If there are more posts, recursively call the function with the pagination token
        if after:
            return recurse(subreddit, hot_list, after)
        else:
            # If there are no more posts, return the hot list
            return hot_list
    else:
        # If subreddit is invalid or request failed, return None
        return None

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Please pass an argument for the subreddit to search.")
    else:
        subreddit = sys.argv[1]
        hot_articles = recurse(subreddit)
        if hot_articles is None:
            print(None)
        else:
            for title in hot_articles:
                print(title)

