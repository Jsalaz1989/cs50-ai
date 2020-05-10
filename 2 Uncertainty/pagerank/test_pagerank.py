import pytest

from pagerank import *


@pytest.mark.parametrize("corpus,page,damping_factor,expected", [
    (
        {"1.html": {"2.html", "3.html"}, "2.html": {"3.html"}, "3.html": {"2.html"}}, 
        "1.html", 
        DAMPING, 
        {'1.html': 0.05, '2.html': 0.475, '3.html': 0.475}
    ),
    (
        {"1.html": {"2.html", "3.html"}, "2.html": {"3.html"}, "3.html": {"2.html"}}, 
        "2.html", 
        DAMPING, 
        {'1.html': 0.05, '2.html': 0.05, '3.html': 0.9}    
    ),
    (
        {"1.html": {"2.html", "3.html"}, "2.html": {"3.html"}, "3.html": {"2.html"}}, 
        "3.html", 
        DAMPING, 
        {'1.html': 0.05, '2.html': 0.9, '3.html': 0.05}    
    )
])
def test_transition_model(corpus, page, damping_factor, expected):
    assert transition_model(corpus, page, damping_factor) == expected


@pytest.mark.parametrize("corpusName,damping_factor,n,tolerance_rank,tolerance_total,expected", [
    (
        "corpus0", 
        DAMPING, 
        SAMPLES,
        0.1,
        0.01,
        {'1.html': 0.2, '2.html': 0.4, '3.html': 0.2, '4.html': 0.1}
    )
])
def test_sample_pagerank(corpusName, damping_factor, n, tolerance_rank, tolerance_total, expected):
    corpus = crawl(corpusName)
    samples_rank = sample_pagerank(corpus, damping_factor, n)
    total = 0
    for page, rank in samples_rank.items():
        assert expected[page] - tolerance_rank <= rank and rank <= expected[page] + tolerance_rank 
        total += rank
    assert 1 - tolerance_total <= total and total <= 1 + tolerance_total


@pytest.mark.parametrize("corpusName,damping_factor,tolerance_rank,tolerance_total,expected", [
    (
        "corpus0", 
        DAMPING, 
        0.1,
        0.01,
        {'1.html': 0.2, '2.html': 0.4, '3.html': 0.2, '4.html': 0.1}
    )
])
def test_iterate_pagerank(corpusName, damping_factor, tolerance_rank, tolerance_total, expected):
    corpus = crawl(corpusName)
    samples_rank = iterate_pagerank(corpus, damping_factor)
    total = 0
    for page, rank in samples_rank.items():
        assert expected[page] - tolerance_rank <= rank and rank <= expected[page] + tolerance_rank 
        total += rank
    assert 1 - tolerance_total <= total and total <= 1 + tolerance_total