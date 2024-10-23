from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import Dict
from dotenv import load_dotenv
import logging

load_dotenv()


class PaperFilter:
    def __init__(self, company_context: Dict):
        self.vectorizer = TfidfVectorizer(stop_words="english")
        self.company_focus = " ".join(
            [
                company_context["industry"],
                " ".join(company_context["research_focus"]),
                " ".join(company_context["current_projects"]),
            ]
        )
        self.min_similarity_threshold = 0.05

    def calculate_relevance(self, paper: Dict) -> float:
        """Calculate relevance score between paper and company focus"""
        paper_text = f"{paper['title']} {paper['summary']}"
        try:
            tfidf_matrix = self.vectorizer.fit_transform(
                [self.company_focus, paper_text]
            )
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            return float(similarity)
        except Exception as e:
            logging.error(f"Relevance calculation error: {e}")
            return 0.0

    def is_relevant(self, paper: Dict) -> bool:
        """Determine if paper is relevant enough to process"""
        relevance_score = self.calculate_relevance(paper)
        return relevance_score >= self.min_similarity_threshold
