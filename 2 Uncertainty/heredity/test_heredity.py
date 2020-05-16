import pytest

from heredity import *


@pytest.mark.parametrize("people,one_gene,two_genes,have_trait,expected", [
    (
        {
            'Harry': {'name': 'Harry', 'mother': 'Lily', 'father': 'James', 'trait': None},
            'James': {'name': 'James', 'mother': None, 'father': None, 'trait': True},
            'Lily': {'name': 'Lily', 'mother': None, 'father': None, 'trait': False}
        }, 
        {"Harry"}, 
        {"James"},
        {"James"},
        0.0026643247488
    )
])
def test_joint_probability(people, one_gene, two_genes, have_trait, expected):
    assert joint_probability(people, one_gene, two_genes, have_trait) == expected