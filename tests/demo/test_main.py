"""Some tests for the main module."""

from itertools import islice

from demo.main import fibo


def test_fibo(fibo_sequence_first_ten):
    """Test fibonacci function."""
    assert list(islice(fibo(), 10)) == fibo_sequence_first_ten
