import os
import random
import re
import sys

# import numpy

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    # print(f'{corpus=}')     ;print(f'{page=}')  ;print(f'{damping_factor=}')
    num_corpus_pages = len(corpus)          #;print(f'{num_corpus_pages=}')
    linked_pages = corpus[page]             #;print(f'{linked_pages=}')
    num_linked_pages = len(corpus[page])    #;print(f'{num_linked_pages=}')

    prob_dist = dict()
    for corpus_page in corpus:
        if corpus_page in linked_pages: prob = (1-DAMPING)/num_corpus_pages + DAMPING/num_linked_pages
        else:                           prob = (1-DAMPING)/num_corpus_pages               
        # prob_dist[corpus_page] = round(prob, 3)
        prob_dist[corpus_page] = prob

    prob_factor = 1 / sum(prob_dist.values())
    prob_dist_normalized = {corpus_page:round(prob_factor*prob,4) for (corpus_page, prob) in prob_dist.items()}

    # print(f'{prob_dist_normalized=}')
    return prob_dist_normalized


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a va              to 1.
    """
    #print(f'{corpus=}')     ;print(f'{damping_factor=}')  ;print(f'{n=}')

    sample = random.choice(list(corpus.keys()))   #;print(f'{sample=}')

    ranks = dict()
    for corpus_page in corpus:
        ranks[corpus_page] = 0
        for sample_num in range(SAMPLES):
            prob_dist = transition_model(corpus, sample, DAMPING)
            sample = random.choices(list(prob_dist.keys()), weights=list(prob_dist.values()))[0]     
            if sample == corpus_page: ranks[corpus_page] += 1
     
        ranks[corpus_page] = ranks[corpus_page] / SAMPLES 

    prob_factor = 1 / sum(ranks.values())
    ranks_normalized = {corpus_page:prob_factor*rank for (corpus_page, rank) in ranks.items()}

    # print(f'{ranks_normalized=}')
    return ranks_normalized


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    #print(f'{corpus=}')     ;print(f'{damping_factor=}')

    num_corpus_pages = len(corpus)          #;print(f'{num_corpus_pages=}')
    ranks = {corpus_page:1/num_corpus_pages for corpus_page in corpus.keys()}
    ranks_current = {corpus_page:0 for corpus_page in corpus.keys()}

    rank_tolerance = 0.001
    converged = False
    while not converged:
        for corpus_page, links in corpus.items():
            pages_linking_to_corpus_page = set(corp_page for (corp_page, links) in corpus.items() if corpus_page in links)
            total = 0
            for page in pages_linking_to_corpus_page:
                total += ranks[page]/len(corpus[page])  
            ranks[corpus_page] = (1-DAMPING)/num_corpus_pages + DAMPING*total
     
        converged = True
        for corpus_page, rank in ranks.items():
            rank_current = ranks_current[corpus_page]
            if not(rank_current - rank_tolerance <= rank and rank <= rank_current + rank_tolerance):
                converged = False
                ranks_current[corpus_page] = rank

    # Normalization method taken from SO: https://stackoverflow.com/questions/26916150/normalize-small-probabilities-in-python
    prob_factor = 1 / sum(ranks.values())
    ranks_normalized = {corpus_page:prob_factor*rank for (corpus_page, rank) in ranks.items()}

    # print(f'{ranks_normalized=}')
    return ranks_normalized


if __name__ == "__main__":
    main()
