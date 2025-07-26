from datetime import datetime, date
import re
from typing import Optional, Tuple
from config import MINIMUM_AGE
import logging

logger = logging.getLogger(__name__)

def calculate_age(dob: date) -> int:
    """
    Calculate age based on date of birth.
    
    Args:
        dob: Date of birth as a date object
        
    Returns:
        int: Age in years
    """
    today = date.today()
    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    return age

def is_age_valid(dob: date) -> Tuple[bool, int]:
    """
    Check if the user meets the minimum age requirement.
    
    Args:
        dob: Date of birth as a date object
        
    Returns:
        Tuple[bool, int]: (is_valid, age_in_years)
    """
    age = calculate_age(dob)
    return age >= MINIMUM_AGE, age

def extract_dob_from_text(text: str) -> Optional[date]:
    """
    Extract date of birth from text using common patterns.
    
    Args:
        text: Text to search for date of birth
        
    Returns:
        Optional[date]: Date of birth if found, None otherwise
    """
    logger.info(f"Starting date extraction from text. Text length: {len(text)}")
    
    # Common date patterns in various formats
    date_patterns = [
        # DD/MM/YYYY or DD-MM-YYYY
        (r'\b(0[1-9]|[12][0-9]|3[01])[/-](0[1-9]|1[0-2])[/-](19|20)\d{2}\b', 
         ['%d/%m/%Y', '%d-%m-%Y']),
        # YYYY/MM/DD or YYYY-MM-DD
        (r'\b(19|20)\d{2}[-/](0[1-9]|1[0-2])[-/](0[1-9]|[12][0-9]|3[01])\b',
         ['%Y/%m/%d', '%Y-%m-%d']),
        # DD Month YYYY (e.g., 01 Jan 1990)
        (r'\b(0[1-9]|[12][0-9]|3[01])\s+(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+(19|20)\d{2}\b',
         ['%d %b %Y', '%d %B %Y'])
    ]
    
    for pattern, formats in date_patterns:
        matches = list(re.finditer(pattern, text, re.IGNORECASE))
        logger.info(f"Pattern '{pattern}' found {len(matches)} matches")
        
        for match in matches:
            date_str = match.group(0)
            logger.info(f"Trying to parse date string: {date_str}")
            
            for fmt in formats:
                try:
                    parsed_date = datetime.strptime(date_str, fmt).date()
                    logger.info(f"Successfully parsed date: {parsed_date} using format: {fmt}")
                    
                    # Basic validation: date should be in the past and not too old
                    today = date.today()
                    if parsed_date > today:
                        logger.warning(f"Future date detected: {parsed_date}")
                        continue
                    if parsed_date.year < 1900:
                        logger.warning(f"Date too old: {parsed_date}")
                        continue
                        
                    return parsed_date
                except ValueError as e:
                    logger.debug(f"Failed to parse '{date_str}' with format '{fmt}': {e}")
                    continue
    
    logger.warning(f"No valid date found in text. Text sample: {text[:200]}...")
    return None

def verify_age(dob: date) -> Tuple[bool, int, bool]:
    """
    Verify if the user meets the minimum age requirement.
    
    Args:
        dob: Date of birth as a date object
        
    Returns:
        Tuple[bool, int, bool]: (is_valid, age, is_minor)
    """
    logger.info(f"Verifying age for DOB: {dob}")
    
    # Calculate age
    today = date.today()
    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    is_valid = age >= MINIMUM_AGE
    is_minor = age < MINIMUM_AGE
    
    logger.info(f"Age calculation: {age} years old. Minimum age: {MINIMUM_AGE}. Valid: {is_valid}")
    
    # Additional logging for debugging
    if age < 0:
        logger.error(f"Negative age calculated. This suggests a date in the future: {dob}")
    elif age > 120:
        logger.warning(f"Unusually old age detected: {age} years. DOB: {dob}")
    
    return is_valid, age, is_minor
