#!/usr/bin/python3
"""
This module provides a recursive function to query the Reddit API, parse the title of all hot articles, and print a sorted count of given keywords.
"""

import requests

def count_words(subreddit, word_list, after=None, counts=None):
    """
    Recursively queries the Reddit API, parses the title of all hot articles, and prints a sorted count of given keywords.

    Args:
        subreddit (str): The name of the subreddit.
        word_list (list): A list of keywords to count.
        after (str): The ID of the last post in the previous page. Used for pagination. Defaults to None.
        counts (dict): A dictionary to store the counts of keywords. Defaults to None.

    Returns:
        None
    """
    if counts is None:
        counts = {}

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
            title = post['data']['title'].lower()
            # Check for each word in the title
            for word in word_list:
                # Ignore words with special characters around them
                if f" {word.lower()} " in title:
                    counts[word.lower()] = counts.get(word.lower(), 0) + 1

        # Get the ID of the last post in the current page for pagination
        after = data['data']['after']

        # If there are more posts, recursively call the function with the pagination token
        if after:
            return count_words(subreddit, word_list, after, counts)
        else:
            # If there are no more posts, print the sorted counts
            sorted_counts = sorted(counts.items(), key=lambda x: (-x[1], x[0]))
            for word, count in sorted_counts:
                print(f"{word}: {count}")
    else:
        # If subreddit is invalid or request failed, print nothing
        pass

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: {} <subreddit> <list of keywords>".format(sys.argv[0]))
        print("Ex: {} programming 'python java javascript'".format(sys.argv[0]))
    else:
        subreddit = sys.argv[1]
        word_list = sys.argv[2].split()
        count_words(subreddit, word_list)

