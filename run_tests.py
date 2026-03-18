"""
Explanation: 
Test runner - runs all tests without needing the -m flag.
"""

import sys
import os



sys.path.insert(0, os.path.dirname(__file__))

def run_test(module_name):
    print(f"\n--- Running {module_name} ---")
    module = __import__(f"tests.{module_name}", fromlist=["main"])
    if hasattr(module, "main"):
        module.main()
    else:
        print(f"Warning: {module_name} has no main() function")

def main():
    # List all test modules (without .py)
    test_modules = [
        "test_chords",
        "test_melody",
        "test_drums",
        "test_midi",
        "test_lyrics",
        "test_markov_lyrics",
        "test_theme_matching",
        "test_edge_cases",
        "verify_all_requirements"
    ]
    for mod in test_modules:
        run_test(mod)

if __name__ == "__main__":
    main()