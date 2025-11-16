"""
🌀 Robust JSON Parser for LLM Outputs
Version: 1.0.0
Created: November 16, 2025

Handles common LLM JSON generation errors:
- Python syntax instead of JSON (None vs null, True/False vs true/false)
- Unquoted string values
- Python comments (#)
- Trailing commas
- Single quotes instead of double quotes
- Truncated JSON (auto-close brackets)

This module is critical for superject learning reliability.
"""

import json
import re
from typing import Tuple, Any, Optional, Dict


def salvage_llm_json(raw_text: str) -> Tuple[Optional[Dict], str, bool]:
    """
    Robust JSON parser for LLM outputs that may contain Python syntax.

    Handles:
    - Unquoted string values: Emiliano → "Emiliano"
    - Python None → JSON null
    - Python True/False → JSON true/false
    - Python comments (#) → removed
    - Trailing commas → removed
    - Single quotes → double quotes
    - Truncated JSON → auto-closed

    Args:
        raw_text: Raw text from LLM that should contain JSON

    Returns:
        Tuple of:
        - parsed_dict: The parsed JSON as dict (None if failed)
        - error_message: Error message if parsing failed (empty string if success)
        - was_salvaged: True if salvage transformations were needed
    """
    if not raw_text or not raw_text.strip():
        return None, "Empty input text", False

    # Step 1: Extract JSON from markdown code blocks if present
    json_str = _extract_json_block(raw_text)
    if json_str is None:
        return None, "No JSON object found in response", False

    # Step 2: Try parsing as-is first (cleanest path)
    try:
        result = json.loads(json_str)
        return result, "", False
    except json.JSONDecodeError:
        pass

    # Step 3: Apply salvage transformations
    salvaged, transformations = _apply_salvage_transformations(json_str)

    # Step 4: Try parsing salvaged JSON
    try:
        result = json.loads(salvaged)
        return result, "", True
    except json.JSONDecodeError as e:
        # Step 5: Try more aggressive salvage
        aggressive_salvaged = _aggressive_salvage(salvaged)
        try:
            result = json.loads(aggressive_salvaged)
            return result, "", True
        except json.JSONDecodeError as e2:
            return None, f"Salvage failed: {str(e2)}", False


def _extract_json_block(raw_text: str) -> Optional[str]:
    """
    Extract JSON object from text, handling markdown code blocks.

    Priority:
    1. ```json ... ``` blocks
    2. ``` ... ``` blocks
    3. Raw { ... } objects
    """
    # Try markdown json blocks first
    json_block_match = re.search(r'```json\s*(\{.*?\})\s*```', raw_text, re.DOTALL)
    if json_block_match:
        return json_block_match.group(1).strip()

    # Try generic markdown blocks
    generic_block_match = re.search(r'```\s*(\{.*?\})\s*```', raw_text, re.DOTALL)
    if generic_block_match:
        return generic_block_match.group(1).strip()

    # Try to find JSON object directly (greedy match for outermost braces)
    # Use non-greedy for nested structures
    brace_depth = 0
    start_idx = -1
    end_idx = -1

    for i, char in enumerate(raw_text):
        if char == '{':
            if brace_depth == 0:
                start_idx = i
            brace_depth += 1
        elif char == '}':
            brace_depth -= 1
            if brace_depth == 0 and start_idx != -1:
                end_idx = i + 1
                break

    if start_idx != -1 and end_idx != -1:
        return raw_text[start_idx:end_idx]

    # Last resort: simple regex
    simple_match = re.search(r'\{.*\}', raw_text, re.DOTALL)
    if simple_match:
        return simple_match.group(0)

    return None


def _apply_salvage_transformations(json_str: str) -> Tuple[str, list]:
    """
    Apply a series of salvage transformations to fix common LLM errors.

    Returns:
        Tuple of (salvaged_string, list_of_transformations_applied)
    """
    salvaged = json_str
    transformations = []

    # 1. Remove Python-style comments (# ...)
    # Be careful not to remove # inside strings
    comment_pattern = r'#[^"\n]*(?=\n|$)'
    if re.search(comment_pattern, salvaged):
        salvaged = re.sub(comment_pattern, '', salvaged)
        transformations.append("removed_python_comments")

    # 2. Replace Python None with JSON null
    # Use word boundary to avoid replacing 'None' inside strings
    if re.search(r'\bNone\b', salvaged):
        salvaged = re.sub(r'\bNone\b', 'null', salvaged)
        transformations.append("replaced_none_with_null")

    # 3. Replace Python True/False with JSON true/false
    if re.search(r'\bTrue\b', salvaged):
        salvaged = re.sub(r'\bTrue\b', 'true', salvaged)
        transformations.append("replaced_true")

    if re.search(r'\bFalse\b', salvaged):
        salvaged = re.sub(r'\bFalse\b', 'false', salvaged)
        transformations.append("replaced_false")

    # 4. Fix unquoted string values in key-value pairs
    # Pattern: "key": unquoted_value -> "key": "unquoted_value"
    # Handles: "value": Emiliano, "context": something
    # Avoid matching numbers, booleans (already fixed), or null
    unquoted_pattern = r'(\"[^\"]+\"\s*:\s*)([A-Za-z_][A-Za-z0-9_]*)((?=\s*[,}\]]))'
    matches = re.findall(unquoted_pattern, salvaged)
    if matches:
        # Don't replace true, false, null
        def replace_unquoted(m):
            key_part = m.group(1)
            value = m.group(2)
            suffix = m.group(3)
            # Skip if already a JSON keyword
            if value in ('true', 'false', 'null'):
                return m.group(0)
            return f'{key_part}"{value}"{suffix}'

        salvaged = re.sub(unquoted_pattern, replace_unquoted, salvaged)
        transformations.append("quoted_unquoted_strings")

    # 4b. Fix "value1" or "value2" patterns (LLM providing alternatives)
    # Pattern: "string1" or "string2" -> "string1/string2" (combine into single value)
    or_pattern = r'"([^"]+)"\s+or\s+"([^"]+)"'
    if re.search(or_pattern, salvaged):
        salvaged = re.sub(or_pattern, r'"\1/\2"', salvaged)
        transformations.append("merged_or_alternatives")

    # 5. Replace single quotes with double quotes
    # This is tricky because of apostrophes in strings
    # Only replace if single quotes are used as string delimiters
    if "'" in salvaged and '"' not in salvaged:
        # JSON uses only double quotes, so if we see single quotes, replace them
        salvaged = salvaged.replace("'", '"')
        transformations.append("replaced_single_quotes")

    # 6. Remove trailing commas before ] or }
    trailing_comma_pattern = r',(\s*[}\]])'
    if re.search(trailing_comma_pattern, salvaged):
        salvaged = re.sub(trailing_comma_pattern, r'\1', salvaged)
        transformations.append("removed_trailing_commas")

    # 7. Clean up excessive whitespace
    salvaged = re.sub(r'\n\s*\n', '\n', salvaged)

    return salvaged, transformations


def _aggressive_salvage(json_str: str) -> str:
    """
    More aggressive salvage for severely malformed JSON.

    Attempts:
    - Auto-close unclosed brackets
    - Fix missing quotes
    - Handle truncated strings
    """
    salvaged = json_str.rstrip()

    # Count open/close brackets
    open_braces = salvaged.count('{')
    close_braces = salvaged.count('}')
    open_brackets = salvaged.count('[')
    close_brackets = salvaged.count(']')
    quote_count = salvaged.count('"')

    # Fix unclosed strings (odd number of quotes)
    if quote_count % 2 == 1:
        # Find the last quote and close the string
        last_quote = salvaged.rfind('"')
        # Add closing quote after reasonable content
        if last_quote > 0:
            salvaged += '"'

    # Auto-close arrays
    while open_brackets > close_brackets:
        salvaged += ']'
        close_brackets += 1

    # Auto-close objects
    while open_braces > close_braces:
        salvaged += '}'
        close_braces += 1

    # Remove any trailing text after the last closing brace
    last_brace = salvaged.rfind('}')
    if last_brace > 0 and last_brace < len(salvaged) - 1:
        salvaged = salvaged[:last_brace + 1]

    return salvaged


def extract_json_safely(raw_text: str, expected_keys: Optional[list] = None) -> Dict:
    """
    Extract JSON from LLM output with validation.

    Args:
        raw_text: Raw LLM output text
        expected_keys: List of keys that must be present in result

    Returns:
        Parsed dict (empty dict if parsing fails)
    """
    result, error, salvaged = salvage_llm_json(raw_text)

    if result is None:
        return {}

    # Validate expected keys if provided
    if expected_keys:
        for key in expected_keys:
            if key not in result:
                # Try to be helpful - maybe key is there with different case
                lower_keys = {k.lower(): k for k in result.keys()}
                if key.lower() in lower_keys:
                    result[key] = result[lower_keys[key.lower()]]

    return result


def format_salvage_report(raw_text: str) -> str:
    """
    Generate a human-readable report of salvage attempts.

    Useful for debugging and monitoring LLM JSON quality.
    """
    json_str = _extract_json_block(raw_text)
    if json_str is None:
        return "No JSON found in text"

    report_lines = [
        "JSON Salvage Report",
        "=" * 40,
        f"Original length: {len(json_str)} chars",
    ]

    # Try original
    try:
        json.loads(json_str)
        report_lines.append("✅ Original JSON is valid")
        return "\n".join(report_lines)
    except json.JSONDecodeError as e:
        report_lines.append(f"❌ Original JSON invalid: {str(e)}")

    # Apply transformations
    salvaged, transformations = _apply_salvage_transformations(json_str)

    if transformations:
        report_lines.append(f"\nTransformations applied ({len(transformations)}):")
        for t in transformations:
            report_lines.append(f"  - {t}")

    # Try salvaged
    try:
        json.loads(salvaged)
        report_lines.append(f"\n✅ Salvaged JSON is valid")
        report_lines.append(f"Salvaged length: {len(salvaged)} chars")
    except json.JSONDecodeError as e:
        report_lines.append(f"\n❌ Salvaged JSON still invalid: {str(e)}")

        # Try aggressive
        aggressive = _aggressive_salvage(salvaged)
        try:
            json.loads(aggressive)
            report_lines.append(f"✅ Aggressive salvage successful")
        except json.JSONDecodeError as e2:
            report_lines.append(f"❌ Aggressive salvage failed: {str(e2)}")

    return "\n".join(report_lines)


# Convenience function for common use case
def parse_llm_json(text: str, fallback: Optional[Dict] = None) -> Dict:
    """
    Parse LLM output as JSON with automatic salvage and fallback.

    Args:
        text: Raw LLM output
        fallback: Default value if parsing fails (default: empty dict)

    Returns:
        Parsed dict or fallback value
    """
    if fallback is None:
        fallback = {}

    result, error, _ = salvage_llm_json(text)
    return result if result is not None else fallback
