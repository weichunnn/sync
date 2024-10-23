import logging
import praw
from typing import List, Dict, Optional
from dotenv import load_dotenv
load_dotenv()


class RedditClient:
    def __init__(self, client_id: str, client_secret: str, user_agent: str):
        self.reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent
        )
        self.llm_subreddits = [
            'MachineLearning',
            'artificial',
            'ChatGPT',
            'OpenAI',
            'LocalLLaMA',
            'Anthropic',
            'AIdev'
        ]
        
    def fetch_posts(self, time_filter: str = 'day', limit: int = 100) -> List[Dict]:
        """Fetch posts from LLM-related subreddits"""
        posts = []
        for subreddit_name in self.llm_subreddits:
            try:
                subreddit = self.reddit.subreddit(subreddit_name)
                for post in subreddit.top(time_filter=time_filter, limit=limit):
                    post_data = {
                        'id': post.id,
                        'subreddit': subreddit_name,
                        'title': post.title,
                        'selftext': post.selftext,
                        'score': post.score,
                        'upvote_ratio': post.upvote_ratio,
                        'num_comments': post.num_comments,
                        'created_utc': post.created_utc,
                        'url': post.url,
                        'comments': self.fetch_comments(post, limit=10)
                    }
                    posts.append(post_data)
            except Exception as e:
                logging.error(f"Error fetching posts from r/{subreddit_name}: {e}")
        return posts

    def fetch_comments(self, post, limit: int = 10) -> List[Dict]:
        """Fetch top comments from a post"""
        comments = []
        post.comments.replace_more(limit=0)  # Remove MoreComments objects
        for comment in post.comments.list()[:limit]:
            try:
                comment_data = {
                    'id': comment.id,
                    'body': comment.body,
                    'score': comment.score,
                    'created_utc': comment.created_utc
                }
                comments.append(comment_data)
            except Exception as e:
                logging.error(f"Error fetching comment {comment.id}: {e}")
        return comments