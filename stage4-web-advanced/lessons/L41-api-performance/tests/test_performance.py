"""Tests for Performance module."""

import pytest
import time
from solutions.solution_01_profiling import QueryAnalyzer, timing_decorator


class TestQueryAnalyzer:
    """Test QueryAnalyzer."""

    def test_record_queries(self):
        """Test recording queries."""
        analyzer = QueryAnalyzer()
        analyzer.record("SELECT * FROM users", 0.01)
        analyzer.record("SELECT * FROM posts", 0.02)

        assert len(analyzer.queries) == 2

    def test_detect_n_plus_one(self):
        """Test N+1 detection."""
        analyzer = QueryAnalyzer()
        for _ in range(5):
            analyzer.record("SELECT * FROM users", 0.01)

        n_plus_one = analyzer.detect_n_plus_one()
        assert "SELECT * FROM users" in n_plus_one

    def test_get_stats(self):
        """Test getting query statistics."""
        analyzer = QueryAnalyzer()
        for _ in range(3):
            analyzer.record("SELECT * FROM users", 0.01)

        stats = analyzer.get_stats()
        assert len(stats) == 1
        assert stats[0].count == 3


class TestTimingDecorator:
    """Test timing decorator."""

    def test_sync_timing(self):
        """Test timing a synchronous function."""

        @timing_decorator
        def slow_func():
            time.sleep(0.01)
            return "done"

        result = slow_func()
        assert result == "done"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
