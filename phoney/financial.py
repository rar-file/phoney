import random
import string
import datetime

__all__ = ['FinancialDataGenerator', 'generate_financial_data']

class FinancialDataGenerator:
    def __init__(self, locale='en_US'):
        self.locale = locale
        
    def generate(self):
        return {
            'credit_card': self._generate_credit_card(),
            'iban': self._generate_iban(),
            'bic': self._generate_bic()
        }
    
    def _generate_credit_card(self):
        issuer = random.choice(['Visa', 'MasterCard', 'American Express', 'Discover'])
        return {
            'issuer': issuer,
            'number': self._generate_credit_card_number(issuer),
            'expiry': self._generate_expiry_date(),
            'cvv': self._generate_cvv(issuer)
        }
    
    def _generate_credit_card_number(self, issuer):
        prefixes = {
            'Visa': ['4'],
            'MasterCard': ['51', '52', '53', '54', '55'],
            'American Express': ['34', '37'],
            'Discover': ['6011', '65']
        }
        
        prefix = random.choice(prefixes[issuer])
        length = 16 if issuer != 'American Express' else 15
        digits = list(prefix) + [str(random.randint(0, 9)) for _ in range(length - len(prefix) - 1)]
        
        # Luhn algorithm implementation
        total = 0
        for i, digit in enumerate(reversed(digits)):
            n = int(digit)
            if i % 2 == 0:
                n *= 2
                total += n - 9 if n > 9 else n
            else:
                total += n
        
        check_digit = (10 - (total % 10)) % 10
        return ''.join(digits) + str(check_digit)
    
    def _generate_expiry_date(self):
        current_year = datetime.datetime.now().year
        return f"{random.randint(1, 12):02d}/{random.randint(current_year + 1, current_year + 5)}"
    
    def _generate_cvv(self, issuer):
        length = 4 if issuer == 'American Express' else 3
        return f"{random.randint(0, 10**length - 1):0{length}d}"
    
    def _generate_iban(self):
        country_codes = {
            'en_US': 'US', 'en_GB': 'GB', 'fr_FR': 'FR', 
            'de_DE': 'DE', 'ja_JP': 'JP', 'zh_CN': 'CN',
            'ko_KR': 'KR', 'ar_EG': 'EG', 'hi_IN': 'IN'
        }
        country = country_codes.get(self.locale, 'US')
        bban = ''.join(random.choices(string.ascii_uppercase + string.digits, k=18))
        iban = f"{country}{random.randint(10,99):02d}{bban}"
        return ' '.join(iban[i:i+4] for i in range(0, len(iban), 4))
    
    def _generate_bic(self):
        country_codes = {
            'en_US': 'US', 'en_GB': 'GB', 'fr_FR': 'FR', 
            'de_DE': 'DE', 'ja_JP': 'JP', 'zh_CN': 'CN',
            'ko_KR': 'KR', 'ar_EG': 'EG', 'hi_IN': 'IN'
        }
        country = country_codes.get(self.locale, 'US')
        bank_code = ''.join(random.choices(string.ascii_uppercase, k=4))
        location = random.choice(['MM', 'FF', 'XX']) + random.choice(string.ascii_uppercase)
        return f"{bank_code}{country}{location}"

def generate_financial_data(locale: str = 'en_US'):
    return FinancialDataGenerator(locale=locale).generate()

# Example usage:
if __name__ == "__main__":
    generator = FinancialDataGenerator(locale='en_US')
    financial_data = generator.generate()
    print(financial_data)
