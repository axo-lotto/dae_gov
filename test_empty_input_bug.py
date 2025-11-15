#!/usr/bin/env python3
"""
Test script to reproduce empty input looping bug.

This simulates the interactive loop to understand why empty inputs
are triggering organism responses.
"""

import sys

def test_input_handling():
    """Test how empty inputs are handled."""

    print("Testing empty input handling...")
    print("Type empty input (just press Enter) to test")
    print("Type 'quit' to exit\n")

    iteration = 0
    while iteration < 10:
        iteration += 1
        print(f"\n=== Iteration {iteration} ===")

        # Simulate rating collection
        print("\n📊 Rate this response:")
        print("  [1] ⭐ Excellent  [2] 👍 Helpful  [3] 👎 Not Helpful  [Enter] Skip")
        rating_input = input("Rating: ").strip()
        print(f"DEBUG: rating_input = '{rating_input}' (len={len(rating_input)})")

        # Simulate main input
        user_input = input("You: ").strip()
        print(f"DEBUG: user_input = '{user_input}' (len={len(user_input)})")

        # Check empty input
        if not user_input:
            print("DEBUG: Empty input detected, should CONTINUE")
            continue

        if user_input == 'quit':
            break

        # Simulate processing
        print(f"PROCESSING: '{user_input}'")

if __name__ == '__main__':
    test_input_handling()
