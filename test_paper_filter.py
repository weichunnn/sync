import pytest
from paper_filter import PaperFilter

# Test data
@pytest.fixture
def company_context():
    return {
        'industry': 'Biotechnology',
        'research_focus': ['Drug Discovery', 'Computational Biology'],
        'current_projects': ['Protein Engineering']
    }

@pytest.fixture
def paper_filter(company_context):
    return PaperFilter(company_context)

@pytest.fixture
def sample_papers():
    return {
        'relevant': {
            'title': 'Drug Discovery Using Machine Learning',
            'summary': 'This paper discusses computational approaches to drug discovery and protein engineering.'
        },
        'irrelevant': {
            'title': 'Economic Market Analysis',
            'summary': 'This paper analyzes stock market trends.'
        }
    }

def test_initialization(company_context):
    """Test if PaperFilter initializes correctly"""
    filter = PaperFilter(company_context)
    assert filter.vectorizer is not None
    assert isinstance(filter.min_similarity_threshold, float)

def test_calculate_relevance(paper_filter, sample_papers):
    """Test relevance calculation for different papers"""
    # Test relevant paper
    relevant_score = paper_filter.calculate_relevance(sample_papers['relevant'])
    assert relevant_score > 0.0
    
    # Test irrelevant paper
    irrelevant_score = paper_filter.calculate_relevance(sample_papers['irrelevant'])
    assert irrelevant_score >= 0.0
    assert irrelevant_score < relevant_score

def test_is_relevant(paper_filter, sample_papers):
    """Test relevance determination"""
    # Relevant paper should return True
    assert paper_filter.is_relevant(sample_papers['relevant']) is True
    
    # Irrelevant paper should return False
    assert paper_filter.is_relevant(sample_papers['irrelevant']) is False

def test_error_handling(paper_filter):
    """Test basic error handling"""
    # Test with empty paper
    empty_paper = {
        'title': '',
        'summary': ''
    }
    score = paper_filter.calculate_relevance(empty_paper)
    assert score >= 0.0
    
    # Test with missing fields
    invalid_paper = {
        'title': 'Test'
        # missing summary field
    }
    with pytest.raises(KeyError):
        paper_filter.calculate_relevance(invalid_paper)