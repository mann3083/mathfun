import random
from typing import List, Dict, Any

class MathGenerator:
    def generate_equation(self) -> List[Dict[str, Any]]:
        # ax + b = c, solve for x
        a = random.randint(2, 12)
        x = random.choice([random.randint(-20, 20), round(random.uniform(-20, 20), 1)])
        b = random.randint(-20, 20)
        c = a * x + b
        # If x is float, ensure only one decimal digit, no rounding off
        if isinstance(x, float):
            x_str = f"{x:.1f}"
        else:
            x_str = str(x)
        question = {
            'id': self._unique_id(),
            'question_text': f"Solve for x: {a}x {'+' if b >= 0 else '-'} {abs(b)} = {c}",
            'type': 'single',
            'correct_answer': x_str
        }
        return [question]
    def __init__(self):
        self.arithmetic_ops = ['+', '-', '*', '/']
        self.friendly_denominators = [2, 4, 5, 8, 10, 20, 25, 50]
        self.generated_ids = set()

    def _unique_id(self):
        while True:
            uid = random.randint(100000, 999999)
            if uid not in self.generated_ids:
                self.generated_ids.add(uid)
                return uid

    def generate_arithmetic(self) -> List[Dict[str, Any]]:
        questions = []
        # One question for each arithmetic type: +, -, *, /
        # Addition
        a, b = random.randint(1000, 9999), random.randint(1000, 9999)
        questions.append({
            'id': self._unique_id(),
            'question_text': f"{a} + {b} = ?",
            'type': 'single',
            'correct_answer': a + b
        })
        # Subtraction
        a, b = sorted([random.randint(1000, 9999), random.randint(1000, 9999)], reverse=True)
        questions.append({
            'id': self._unique_id(),
            'question_text': f"{a} - {b} = ?",
            'type': 'single',
            'correct_answer': a - b
        })
        # Multiplication (ensure product <= 9999)
        # Find all (a, b) pairs where 1000 <= a <= 9999, 2 <= b <= 9, a * b <= 9999
        # To simplify, pick b first, then restrict a
        b = random.randint(2, 9)
        max_a = min(9999, 9999 // b)
        min_a = max(1000, 1000 // b + (1 if 1000 % b else 0))
        if min_a > max_a:
            min_a = 1000
            max_a = 9999 // b
        a = random.randint(min_a, max_a)
        questions.append({
            'id': self._unique_id(),
            'question_text': f"{a} × {b} = ?",
            'type': 'single',
            'correct_answer': a * b
        })
        # Division
        divisor = random.randint(2, 99)
        dividend = random.randint(1000, 9999)
        quotient = dividend // divisor
        remainder = dividend % divisor
        questions.append({
            'id': self._unique_id(),
            'question_text': f"Divide {dividend} by {divisor}. What is the Quotient and Remainder?",
            'type': 'dual',
            'correct_answer': {'quotient': quotient, 'remainder': remainder}
        })
        return questions

    def generate_factorization(self) -> List[Dict[str, Any]]:
        n = random.randint(10, 499)
        factors = self.prime_factors(n)
        return [{
            'id': self._unique_id(),
            'question_text': f"List all prime factors of {n} (comma separated)",
            'type': 'text',
            'correct_answer': ','.join(map(str, factors))
        }]

    def prime_factors(self, n: int) -> List[int]:
        i = 2
        factors = []
        while i * i <= n:
            while n % i == 0:
                factors.append(i)
                n //= i
            i += 1
        if n > 1:
            factors.append(n)
        return factors

    def generate_conversions(self) -> List[Dict[str, Any]]:
        mode = random.choice(['frac2dec', 'dec2perc', 'perc2frac'])
        if mode == 'frac2dec':
            denom = random.choice(self.friendly_denominators)
            numer = random.randint(1, denom - 1)
            dec = round(numer / denom, 4)
            return [{
                'id': self._unique_id(),
                'question_text': f"Convert {numer}/{denom} to decimal.",
                'type': 'single',
                'correct_answer': dec
            }]
        elif mode == 'dec2perc':
            denom = random.choice(self.friendly_denominators)
            numer = random.randint(1, denom - 1)
            dec = round(numer / denom, 4)
            perc = round(dec * 100, 2)
            return [{
                'id': self._unique_id(),
                'question_text': f"Convert {dec} to percentage.",
                'type': 'single',
                'correct_answer': perc
            }]
        else:  # perc2frac
            denom = random.choice(self.friendly_denominators)
            numer = random.randint(1, denom - 1)
            perc = round((numer / denom) * 100, 2)
            return [{
                'id': self._unique_id(),
                'question_text': f"Convert {perc}% to fraction (as a/b, lowest terms)",
                'type': 'text',
                'correct_answer': self._lowest_terms(numer, denom)
            }]

    def _gcd(self, a, b):
        while b:
            a, b = b, a % b
        return a

    def _lowest_terms(self, numer, denom):
        g = self._gcd(numer, denom)
        return f"{numer // g}/{denom // g}"

    def generate_mixed(self) -> List[Dict[str, Any]]:
        # One random from any type
        pool = self.generate_arithmetic() + self.generate_factorization() + self.generate_conversions()
        random.shuffle(pool)
        return [pool[0]]

    def generate_all(self) -> List[Dict[str, Any]]:
        # Target: 10 questions, equal segments (5 segments -> 2 each)
        segments = []
        
        # 1. Arithmetic: Pick 2 distinct
        arith = self.generate_arithmetic()
        segments.extend(random.sample(arith, 2))
        
        # 2. Factorization: Generate 2
        for _ in range(2):
            segments.extend(self.generate_factorization())
            
        # 3. Conversions: Generate 2
        for _ in range(2):
            segments.extend(self.generate_conversions())
            
        # 4. Mixed: Generate 2
        for _ in range(2):
            segments.extend(self.generate_mixed())
            
        # 5. Equations: Generate 2
        for _ in range(2):
            segments.extend(self.generate_equation())

        random.shuffle(segments)
        return segments
