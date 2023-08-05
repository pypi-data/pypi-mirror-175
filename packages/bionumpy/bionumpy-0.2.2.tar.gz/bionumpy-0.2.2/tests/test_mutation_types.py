import pytest
from bionumpy.mutation_signature import count_mutation_types
from bionumpy.datatypes import Variant


@pytest.fixture
def snps():
    return Variant(["chr1"]*3, [2, 3, 6], ["A", "C", "G"], ["T", "G", "A"])


@pytest.fixture
def reference():
    return "CCACCCGT"


def test_count_mutation_types(snps, reference):
    counts = count_mutation_types(snps, reference)
    print(counts)
    for t in ["G[T>A]G", "A[C>G]C", "A[C>T]G"]:
        assert counts[t] == 1
    assert counts.counts.sum() == len(snps)
