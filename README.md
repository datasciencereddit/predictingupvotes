# predictingupvotes

This group of files and data was used in a data science project. Download the zip file to get started.

badEntryDeleter.py deletes entries from the data that do not end with a date. Helped during certain situations.

DuplicateChecker.py is a script that can be run seperately, or is used everytime data is scraped from reddit. This is used to prevent duplicate entries in the data.

redditScraped.txt is the data from r/popular we gathered to make our models in r. The attributes include a posts: id, title, author name, upvotes, upvote ratio, number of comments,
subreddit, and time of upload in that order.

redditScrapedBackup04132021.txt is a text file that was used to backup some of the data.

RedditScraperTemplate.py was the scraper that used the PRAW package for python that used the Reddit API for data scraping with the permission of Reddit. It requires a reddit account to
log in to whenever the user would like to use it.

titlevalue.txt is every value from redditScraped.txt in order and displays a range of numbers from 0 to 1. These values determine how signifigant a title might be depending on
keywords within the title.

wordEvaluator.py uses redditScraped.txt to create titlevalue.txt. It averages the amount of upvotes per word and averages the upvote ratios per word. Then, it uses all of
those values to create a wordvalue for each word by multiplying both of those averages together. Then, it will go through every title and determine it's average word value based
on the words in the title. Finally, it will print those values to titlevalue.txt.
