"""
Entity Extraction Engine
Extracts intelligence from conversations (bank accounts, UPI IDs, URLs, phone numbers)
"""

import re
from typing import Dict, List, Any
import logging

logger = logging.getLogger(__name__)


class EntityExtractor:
    """Extracts and validates entities from scam conversations"""
    
    def __init__(self):
        # Indian bank account patterns
        self.bank_account_pattern = re.compile(r'\b\d{9,18}\b')
        
        # IFSC code pattern (4 letters + 0 + 6 alphanumeric)
        self.ifsc_pattern = re.compile(r'\b[A-Z]{4}0[A-Z0-9]{6}\b', re.IGNORECASE)
        
        # UPI ID pattern
        self.upi_pattern = re.compile(r'\b[\w\.\-]+@[\w]+\b')
        
        # Known UPI handles for validation
        self.known_upi_handles = [
            'paytm', 'ybl', 'oksbi', 'axl', 'icici', 'hdfcbank', 'ibl',
            'okaxis', 'okhdfcbank', 'okicici', 'sbi', 'upi', 'pnb',
            'boi', 'cnrb', 'unionbank', 'indianbank', 'sc', 'federal'
        ]
        
        # Indian mobile number pattern (starts with 6-9, 10 digits)
        self.phone_pattern = re.compile(r'\b[6-9]\d{9}\b')
        
        # URL patterns
        self.url_pattern = re.compile(
            r'https?://[^\s]+|www\.[^\s]+|[a-zA-Z0-9-]+\.(com|in|org|net|co\.in|info|xyz|tk|ml|ga|cf|gq)[^\s]*',
            re.IGNORECASE
        )
        
        # Name extraction patterns
        self.name_patterns = [
            re.compile(r'(?:name|account holder|beneficiary)[\s:]+([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,3})', re.IGNORECASE),
            re.compile(r'\b([A-Z][a-z]+\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\b')
        ]
    
    def extract(self, messages: List[str]) -> Dict[str, Any]:
        """
        Extract all intelligence from conversation messages
        
        Args:
            messages: List of all messages in the conversation
            
        Returns:
            Dictionary with extracted entities and metadata
        """
        # Combine all messages
        full_text = " ".join(messages)
        
        # Extract each entity type
        bank_accounts = self._extract_bank_accounts(full_text)
        upi_ids = self._extract_upi_ids(full_text)
        phone_numbers = self._extract_phone_numbers(full_text)
        urls = self._extract_urls(full_text)
        names = self._extract_names(full_text)
        
        # Build extracted data structure
        extracted_data = {}
        
        if bank_accounts:
            extracted_data["bank_accounts"] = bank_accounts
        
        if upi_ids:
            extracted_data["upi_ids"] = upi_ids
        
        if phone_numbers:
            extracted_data["phone_numbers"] = phone_numbers
        
        if urls:
            extracted_data["urls"] = urls
        
        if names:
            extracted_data["names"] = names
        
        # Calculate total extraction count
        extraction_count = (
            len(bank_accounts) + len(upi_ids) + 
            len(phone_numbers) + len(urls) + len(names)
        )
        
        logger.info(f"Extracted {extraction_count} entities: {len(bank_accounts)} bank accounts, "
                   f"{len(upi_ids)} UPI IDs, {len(phone_numbers)} phones, "
                   f"{len(urls)} URLs, {len(names)} names")
        
        return {
            "extracted_data": extracted_data,
            "extraction_count": extraction_count
        }
    
    def _extract_bank_accounts(self, text: str) -> List[Dict[str, Any]]:
        """Extract bank account numbers with IFSC codes"""
        accounts = []
        seen_accounts = set()
        
        # Find all potential account numbers
        account_matches = self.bank_account_pattern.findall(text)
        
        # Find all IFSC codes
        ifsc_matches = self.ifsc_pattern.findall(text)
        
        for account in account_matches:
            # Skip if already seen or too short/long
            if account in seen_accounts or len(account) < 9 or len(account) > 18:
                continue
            
            seen_accounts.add(account)
            
            # Try to find associated IFSC code
            ifsc_code = ifsc_matches[0] if ifsc_matches else None
            
            # Try to find account holder name
            holder_name = self._find_nearby_name(text, account)
            
            # Calculate confidence
            confidence = 0.6  # Base confidence
            if ifsc_code:
                confidence += 0.3  # IFSC code present
            if holder_name:
                confidence += 0.1  # Name present
            
            account_data = {
                "account_number": account,
                "confidence": round(min(confidence, 1.0), 2)
            }
            
            if ifsc_code:
                account_data["ifsc_code"] = ifsc_code.upper()
            
            if holder_name:
                account_data["account_holder"] = holder_name
            
            accounts.append(account_data)
        
        return accounts
    
    def _extract_upi_ids(self, text: str) -> List[Dict[str, Any]]:
        """Extract UPI IDs"""
        upi_ids = []
        seen_upis = set()
        
        matches = self.upi_pattern.findall(text)
        
        for upi in matches:
            # Skip emails and already seen
            if upi in seen_upis or '@gmail' in upi.lower() or '@yahoo' in upi.lower():
                continue
            
            seen_upis.add(upi)
            
            # Extract handle
            handle = upi.split('@')[1].lower() if '@' in upi else ''
            
            # Calculate confidence based on known handles
            confidence = 0.95 if handle in self.known_upi_handles else 0.7
            
            upi_ids.append({
                "upi_id": upi,
                "confidence": confidence
            })
        
        return upi_ids
    
    def _extract_phone_numbers(self, text: str) -> List[Dict[str, Any]]:
        """Extract Indian phone numbers"""
        phones = []
        seen_phones = set()
        
        matches = self.phone_pattern.findall(text)
        
        for phone in matches:
            if phone in seen_phones:
                continue
            
            seen_phones.add(phone)
            
            phones.append({
                "number": phone,
                "confidence": 0.7  # Medium confidence (could be fake)
            })
        
        return phones
    
    def _extract_urls(self, text: str) -> List[Dict[str, Any]]:
        """Extract URLs and phishing links"""
        urls = []
        seen_urls = set()
        
        matches = self.url_pattern.findall(text)
        
        for url in matches:
            if isinstance(url, tuple):
                url = url[0] if url[0] else url[1]
            
            if url in seen_urls:
                continue
            
            seen_urls.add(url)
            
            # Extract domain
            domain = self._extract_domain(url)
            
            # Check for suspicious indicators
            is_suspicious = self._is_suspicious_url(url, domain)
            
            confidence = 0.9 if is_suspicious else 0.8
            
            url_data = {
                "url": url,
                "confidence": confidence
            }
            
            if domain:
                url_data["domain"] = domain
            
            urls.append(url_data)
        
        return urls
    
    def _extract_names(self, text: str) -> List[Dict[str, Any]]:
        """Extract names from text"""
        names = []
        seen_names = set()
        
        for pattern in self.name_patterns:
            matches = pattern.findall(text)
            for match in matches:
                name = match if isinstance(match, str) else match[0]
                name = name.strip()
                
                # Skip if already seen or too short
                if name in seen_names or len(name) < 4:
                    continue
                
                # Skip common words
                if name.lower() in ['dear sir', 'dear madam', 'hello sir', 'thank you']:
                    continue
                
                seen_names.add(name)
                
                names.append({
                    "name": name,
                    "confidence": 0.6  # Low confidence (easily faked)
                })
        
        return names
    
    def _find_nearby_name(self, text: str, account: str) -> str:
        """Find name near account number"""
        # Look for name within 50 characters before or after account number
        account_pos = text.find(account)
        if account_pos == -1:
            return None
        
        context = text[max(0, account_pos - 50):account_pos + 50]
        
        for pattern in self.name_patterns:
            match = pattern.search(context)
            if match:
                return match.group(1) if isinstance(match.group(1), str) else match.group(0)
        
        return None
    
    def _extract_domain(self, url: str) -> str:
        """Extract domain from URL"""
        # Remove protocol
        domain = re.sub(r'^https?://', '', url)
        domain = re.sub(r'^www\.', '', domain)
        
        # Get domain part (before first /)
        domain = domain.split('/')[0]
        domain = domain.split('?')[0]
        
        return domain
    
    def _is_suspicious_url(self, url: str, domain: str) -> bool:
        """Check if URL looks suspicious"""
        suspicious_indicators = [
            '.tk', '.ml', '.ga', '.cf', '.gq',  # Free TLDs
            'bit.ly', 'tinyurl', 'short',  # URL shorteners
            'login', 'verify', 'secure', 'update',  # Phishing keywords
            'account-', 'banking-', 'payment-'  # Suspicious patterns
        ]
        
        url_lower = url.lower()
        return any(indicator in url_lower for indicator in suspicious_indicators)
