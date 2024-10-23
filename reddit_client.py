import logging
import praw
from typing import List, Dict, Optional
from dotenv import load_dotenv
from datetime import datetime, timedelta
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
load_dotenv()


class RedditClient:
    def __init__(self, client_id: str, client_secret: str, user_agent: str, prompt: str):
        if not client_id or not client_secret:
            raise ValueError("Reddit API credentials are required")
            
        try:
            self.reddit = praw.Reddit(
                client_id=client_id,
                client_secret=client_secret,
                user_agent=user_agent
            )
            # Verify authentication
            self.reddit.user.me()
            logging.info("Successfully authenticated with Reddit API")
        except Exception as e:
            logging.error(f"Failed to initialize Reddit client: {e}")
            raise
            
        self.llm_subreddits = [
            'MachineLearning',
            'artificial',
            'ChatGPT',
            'OpenAI',
            'LocalLLaMA',
            'Anthropic',
            'AIdev',
            'LangChain',
            'bioinformatics',  # Added biotech-specific subreddits
            'StableDiffusion',
            'MLOps'
        ]
        self.prompt = prompt
        self.vectorizer = TfidfVectorizer(stop_words='english',ngram_range=(1, 2))
        logging.info(f"Monitoring subreddits: {', '.join(self.llm_subreddits)}")

    def fetch_posts(self, company_context: Dict, time_filter: str = 'day', limit: int = 100) -> List[Dict]:
        """Fetch posts from LLM-related subreddits from the past 48 hours"""
        posts = []
        cutoff_time = datetime.now() - timedelta(hours=48)
        total_fetched = 0
        relevant_count = 0
        
        try:
            # Create a multireddit-style query
            subreddits_combined = '+'.join(self.llm_subreddits)
            subreddit = self.reddit.subreddit(subreddits_combined)
            
            # Try different sorting methods to get more posts
            for sort_method in ['hot', 'new', 'top']:
                logging.info(f"Fetching {sort_method} posts from r/{subreddits_combined}")
                
                if sort_method == 'top':
                    submission_stream = subreddit.top(time_filter='week', limit=limit)
                elif sort_method == 'hot':
                    submission_stream = subreddit.hot(limit=limit)
                else:
                    submission_stream = subreddit.new(limit=limit)
                
                for post in submission_stream:
                    total_fetched += 1
                    
                    try:
                        # Skip if post is older than 48 hours
                        post_time = datetime.fromtimestamp(post.created_utc)
                        if post_time < cutoff_time:
                            continue
                        
                        # Calculate relevance score using company context
                        combined_text = f"{post.title} {post.selftext}"
                        relevance_score = self.calculate_relevance(combined_text, company_context)
                        
                        # Only include posts with relevance score above threshold
                        if relevance_score >= 0.01:  # Adjust threshold as needed
                            relevance_score*=82
                            relevant_count += 1
                            
                            # Get top comments
                            post.comments.replace_more(limit=0)
                            comments = []
                            for comment in post.comments.list()[:10]:
                                try:
                                    comments.append({
                                        'id': comment.id,
                                        'body': comment.body,
                                        'score': comment.score,
                                        'created_utc': comment.created_utc
                                    })
                                except Exception as e:
                                    logging.warning(f"Error processing comment {comment.id}: {e}")
                            
                            post_data = {
                                'metadata': {
                                    'id': post.id,
                                    'subreddit': post.subreddit.display_name,
                                    'created_utc': post.created_utc,
                                    'processed_at': datetime.now().isoformat(),
                                    'url': f"https://reddit.com{post.permalink}",
                                    'relevance_score': relevance_score,
                                    'company_context': {
                                        'industry': company_context['industry'],
                                        'research_focus': company_context['research_focus']
                                    }
                                },
                                'content': {
                                    'title': post.title,
                                    'selftext': post.selftext,
                                    'score': post.score,
                                    'upvote_ratio': post.upvote_ratio,
                                    'num_comments': post.num_comments,
                                    'comments': comments
                                }
                            }
                            posts.append(post_data)
                            
                            logging.debug(f"Added relevant post: '{post.title[:50]}...' (score: {relevance_score:.2f})")
                    
                    except Exception as e:
                        logging.warning(f"Error processing post {post.id}: {e}")
                        continue
                
                if posts:  # If we have enough posts, no need to try other sorting methods
                    break
        
        except Exception as e:
            logging.error(f"Error fetching posts: {e}")
        
        finally:
            logging.info(f"Fetched {total_fetched} total posts, found {relevant_count} relevant posts")
        
        return posts

    def calculate_relevance(self, text: str, company_context: Dict) -> float:
        """Calculate relevance score between post and company context"""
        try:
            # Create a comprehensive context string
            context_terms = [
                company_context['industry'],
                *company_context['research_focus'],
                *company_context['current_projects'],
                *company_context.get('core_technologies', []),
                *company_context.get('available_resources', [])
            ]
            
            # Add related terms for each context term
            expanded_terms = []
            for term in context_terms:
                expanded_terms.extend([
                    term,
                    term.lower(),
                    term.replace(' ', ''),
                    term.replace('-', ' ')
                ])
            
            context_string = ' '.join(expanded_terms)
            
            # Calculate similarity
            tfidf_matrix = self.vectorizer.fit_transform([context_string, text])
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            
            return float(similarity)
            
        except Exception as e:
            logging.error(f"Error calculating relevance: {e}")
            return 0.0