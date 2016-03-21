import os
import time
import praw
import datetime

class RedditCounter(object):
    def __init__(self, subreddit):
        start_time = time.time()
        user_agent = "RedditCounter 0.0.1"
        self.reddit = praw.Reddit(user_agent=user_agent)
        self.subreddit = subreddit
        self.subreddits_dict = {}
        self.nsfw_count = 0
        self.amount = 1000
        self.count_subreddits()
        print "Finished in {0:.3g} seconds".format(time.time() - start_time)

    def get_posts(self):
        print "Getting posts..."
        subreddit = self.reddit.get_subreddit(self.subreddit)
        return subreddit.get_hot(limit=self.amount)
        print "Done getting posts..."

    def count_subreddits(self):
        posts = self.get_posts()
        print "Counting posts..."
        for post in posts:
            sub = post.subreddit
            name = sub.display_name
            if post.over_18:
                self.nsfw_count += 1
            if name in self.subreddits_dict:
                self.subreddits_dict[name] += 1
            else:
                self.subreddits_dict[name] = 1
        self.dump_to_file()

    def dump_to_file(self):
        date = datetime.datetime.now().date()
        file_name = str(date)
        time = datetime.datetime.now().time().strftime("%H")
        items = self.subreddits_dict.iteritems()
        total_subreddits = len(self.subreddits_dict)
        nsfw_percent = (self.nsfw_count / float(self.amount)) * 100
        nsfw_percent = "{0:.3g}".format(nsfw_percent)
        output = ["{},{}".format(sub, count) for sub, count in items]
        output = ",".join(output)
        path = "G:\RandomCode\Python\RedditBots\RedditCounts\SubredditCounts"
        os.chdir(path)
        print "Dumping to {}\{}".format(path, file_name)
        with open(file_name, 'a+') as f:
            f.write("{},  {}:00\n".format(date, time))
            f.write("Subreddits seen,{}\n".format(total_subreddits))
            f.write("NSFW: ({} / {}), {}%\n".format(self.nsfw_count, self.amount, nsfw_percent))
            f.write(output)
            f.write("\n")

rc = RedditCounter('all')
# r = praw.Reddit(user_agent="Reddit counter")
# s = r.get_subreddit('all')
# posts = s.get_hot(limit=1000)
# print len(list(posts))
# for post in posts:
#     subreddit = post.subreddit
#     print subreddit.display_name
