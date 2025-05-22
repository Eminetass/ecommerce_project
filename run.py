import sys
import pytest
from app import create_app

app = create_app()

def run_tests():
    """Run all tests with pytest"""
    pytest.main([
        'tests',  # test directory
        '-v',     # verbose output
        '--cov=app',  # coverage report for app directory
        '--cov-report=term-missing'  # show lines that need test coverage
    ])

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        run_tests()
    else:
        app.run(debug=True) 