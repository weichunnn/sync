import json
from anthropic import Anthropic
from textblob import TextBlob
import xml.etree.ElementTree as ET
from typing import Dict, List, Optional
import logging
from dotenv import load_dotenv
import nltk
import re
from collections import Counter
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
load_dotenv()

# Download required NLTK data
def ensure_nltk_resources():
    """Ensure all required NLTK resources are downloaded"""
    required_resources = [
        'punkt',
        'stopwords',
        'wordnet',
        'averaged_perceptron_tagger',
        'punkt_tab'
    ]
    
    for resource in required_resources:
        try:
            nltk.data.find(f'tokenizers/{resource}')
        except LookupError:
            try:
                nltk.download(resource, quiet=True)
                logging.info(f"Successfully downloaded NLTK resource: {resource}")
            except Exception as e:
                logging.error(f"Error downloading NLTK resource {resource}: {e}")
                raise RuntimeError(f"Failed to download required NLTK resource: {resource}")

class SentimentAnalyzer:
    def __init__(self):
        # Ensure NLTK resources are available before initializing
        try:
            ensure_nltk_resources()
        except Exception as e:
            logging.error(f"Failed to initialize NLTK resources: {e}")
            raise

        self.stop_words = set(stopwords.words('english'))
        self.lemmatizer = WordNetLemmatizer()
        
        # Key phrases for different aspects of LLM discussion
        self.aspect_keywords = {
            'performance': ['fast', 'slow', 'speed', 'quick', 'lag', 'responsive', 'efficient', 'performance'],
            'accuracy': ['accurate', 'wrong', 'mistake', 'correct', 'error', 'precise', 'accuracy'],
            'cost': ['expensive', 'cheap', 'cost', 'price', 'affordable', 'pricing', 'subscription'],
            'features': ['feature', 'capability', 'function', 'ability', 'support', 'integration'],
            'reliability': ['reliable', 'stable', 'crash', 'bug', 'issue', 'problem', 'consistent'],
            'user_experience': ['intuitive', 'easy', 'difficult', 'confusing', 'simple', 'complex', 'user-friendly'],
            'technical': ['api', 'code', 'programming', 'implementation', 'software', 'development', 'technical'],
            'business': ['enterprise', 'business', 'company', 'corporate', 'industry', 'commercial', 'market']
        }
        
        # Sentiment modifiers
        self.sentiment_modifiers = {
            'positive': ['good', 'great', 'excellent', 'amazing', 'awesome', 'fantastic', 'helpful', 'useful'],
            'negative': ['bad', 'terrible', 'poor', 'horrible', 'awful', 'useless', 'waste', 'disappointing'],
            'neutral': ['okay', 'average', 'moderate', 'fair', 'decent']
        }

    def preprocess_text(self, text: str) -> str:
        """Preprocess text for analysis"""
        # Convert to lowercase and remove special characters
        text = re.sub(r'[^a-zA-Z\s]', ' ', text.lower())
        
        try:
            # Tokenize and lemmatize
            tokens = word_tokenize(text)
            tokens = [self.lemmatizer.lemmatize(token) for token in tokens if token not in self.stop_words]
            return ' '.join(tokens)
        except Exception as e:
            logging.error(f"Error in text preprocessing: {e}")
            # Return cleaned text even if tokenization fails
            return text

    def extract_key_phrases(self, text: str) -> Dict[str, List[str]]:
        """Extract key phrases related to different aspects"""
        try:
            preprocessed_text = self.preprocess_text(text)
            sentences = sent_tokenize(text)
            
            aspects = {aspect: [] for aspect in self.aspect_keywords.keys()}
            
            for sentence in sentences:
                sentence_lower = sentence.lower()
                for aspect, keywords in self.aspect_keywords.items():
                    if any(keyword in sentence_lower for keyword in keywords):
                        aspects[aspect].append(sentence.strip())
            
            return aspects
        except Exception as e:
            logging.error(f"Error in key phrase extraction: {e}")
            return {aspect: [] for aspect in self.aspect_keywords.keys()}

    def analyze_sentiment(self, content: Dict) -> Dict:
        """Perform comprehensive sentiment analysis with error handling"""
        try:
            # Combine title, post content, and top comments
            full_text = f"{content['title']} {content['selftext']}"
            for comment in content['comments'][:3]:  # Analyze top 3 comments
                full_text += f" {comment['body']}"
            
            # Basic sentiment analysis
            blob = TextBlob(full_text)
            basic_sentiment = {
                'polarity': float(blob.sentiment.polarity),
                'subjectivity': float(blob.sentiment.subjectivity)
            }
            
            # Extract aspects and their sentiments
            aspects = self.extract_key_phrases(full_text)
            aspect_sentiments = {}
            
            for aspect, sentences in aspects.items():
                if sentences:
                    aspect_sentiment = sum(TextBlob(sent).sentiment.polarity for sent in sentences) / len(sentences)
                    aspect_sentiments[aspect] = {
                        'sentiment_score': float(aspect_sentiment),
                        'example_quotes': sentences[:2]  # Include up to 2 example quotes
                    }
            
            # Extract feature requests using simple pattern matching
            feature_requests = []
            try:
                sentences = sent_tokenize(full_text)
                feature_requests = [
                    sent.strip() for sent in sentences
                    if any(word in sent.lower() for word in ['should', 'could', 'wish', 'hope', 'need', 'want'])
                    and any(word in sent.lower() for word in ['feature', 'add', 'implement', 'include', 'support'])
                ]
            except Exception as e:
                logging.error(f"Error extracting feature requests: {e}")
            
            # Calculate engagement metrics
            engagement_score = (content['score'] + content['num_comments']) / (content['upvote_ratio'] if content['upvote_ratio'] > 0 else 1)
            
            # Prepare final analysis
            analysis = {
                'basic_sentiment': basic_sentiment,
                'aspect_sentiments': aspect_sentiments,
                'feature_requests': feature_requests[:3],  # Top 3 feature requests
                'engagement_metrics': {
                    'score': content['score'],
                    'comments': content['num_comments'],
                    'upvote_ratio': content['upvote_ratio'],
                    'engagement_score': float(engagement_score)
                },
                'summary_stats': {
                    'total_aspects_mentioned': len([asp for asp, sent in aspects.items() if sent]),
                    'dominant_aspect': max(aspects.items(), key=lambda x: len(x[1]))[0] if any(aspects.values()) else None,
                    'overall_sentiment': 'positive' if basic_sentiment['polarity'] > 0.1 
                                       else 'negative' if basic_sentiment['polarity'] < -0.1 
                                       else 'neutral'
                }
            }
            
            return analysis
        except Exception as e:
            logging.error(f"Error in sentiment analysis: {e}")
            # Return a minimal analysis in case of errors
            return {
                'basic_sentiment': {'polarity': 0.0, 'subjectivity': 0.0},
                'aspect_sentiments': {},
                'feature_requests': [],
                'engagement_metrics': {
                    'score': content['score'],
                    'comments': content['num_comments'],
                    'upvote_ratio': content['upvote_ratio'],
                    'engagement_score': 0.0
                },
                'summary_stats': {
                    'total_aspects_mentioned': 0,
                    'dominant_aspect': None,
                    'overall_sentiment': 'neutral'
                }
            }