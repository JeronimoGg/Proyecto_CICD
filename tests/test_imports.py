def test_import_os():
    """Test to verify os import works correctly"""
    import os
    assert hasattr(os, 'environ')
    # os.environ is not a dict, it's a mapping object
    assert hasattr(os.environ, 'get')
    assert hasattr(os.environ, 'keys')
    assert 'TESTING' not in os.environ  # Should not be set by default
