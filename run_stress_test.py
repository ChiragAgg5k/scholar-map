#!/usr/bin/env python3
"""
Simple runner script for Scholar Map stress testing.

This script runs the stress test data generator with common configurations.
"""

import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.stress_test_data import main

if __name__ == "__main__":
    sys.exit(main())
