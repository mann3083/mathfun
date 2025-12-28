import random
import json
import os
import math
from typing import List, Dict, Any

class MathGenerator:
    def __init__(self):
        self.friendly_denominators = [2, 4, 5, 8, 10, 20, 25, 50]
        self.generated_ids = set()
        self.scenarios = self._load_data()

    def _load_data(self):
        """Loads creative scenarios from scenarios.json or uses defaults."""
        default_data = {
            "unitary_work_scenarios": [{"actor": "workers", "task": "build a wall"}],
            "profit_loss_items": ["item"],
            "profit_loss_names": ["Shopkeeper"],
            "unitary_cost_items": ["apples"],
            "di_topics": [{"title": "Data", "labels": ["A", "B"], "unit": "Val"}],
            "ds_problems": [{"question": "Find X", "stat1": "X=1", "stat2": "Y=2", "correct": "Only I"}],
            "lr_coding_words": ["CODE"]
        }
        try:
            file_path = os.path.join(os.path.dirname(__file__), 'scenarios.json')
            if os.path.exists(file_path):
                with open(file_path, 'r') as f:
                    return json.load(f)
            else:
                return default_data
        except Exception:
            return default_data

    def _unique_id(self):
        while True:
            uid = random.randint(100000, 999999)
            if uid not in self.generated_ids:
                self.generated_ids.add(uid)
                return uid

    def _gcd(self, a, b):
        while b: a, b = b, a % b
        return a

    def _lowest_terms(self, numer, denom):
        g = self._gcd(numer, denom)
        return f"{numer // g}/{denom // g}"

    # --- 1. ADDITION ---
    def generate_addition(self) -> List[Dict[str, Any]]:
        a = random.randint(1000, 9999)
        b = random.randint(1000, 9999)
        return [{
            'id': self._unique_id(),
            'question_text': f"{a} + {b} = ?",
            'type': 'single',
            'correct_answer': a + b,
            'category': 'Addition'
        }]

    # --- 2. SUBTRACTION ---
    def generate_subtraction(self) -> List[Dict[str, Any]]:
        a, b = sorted([random.randint(1000, 9999), random.randint(1000, 9999)], reverse=True)
        return [{
            'id': self._unique_id(),
            'question_text': f"{a} - {b} = ?",
            'type': 'single',
            'correct_answer': a - b,
            'category': 'Subtraction'
        }]

    # --- 3. MULTIPLICATION ---
    def generate_multiplication(self) -> List[Dict[str, Any]]:
        b = random.randint(2, 9)
        max_a = min(9999, 9999 // b)
        min_a = max(1000, 1000 // b + (1 if 1000 % b else 0))
        if min_a > max_a: min_a, max_a = 1000, 9999 // b
        a = random.randint(min_a, max_a)
        return [{
            'id': self._unique_id(),
            'question_text': f"{a} × {b} = ?",
            'type': 'single',
            'correct_answer': a * b,
            'category': 'Multiplication'
        }]

    # --- 4. DIVISION ---
    def generate_division(self) -> List[Dict[str, Any]]:
        divisor = random.randint(2, 99)
        dividend = random.randint(1000, 9999)
        quotient = dividend // divisor
        remainder = dividend % divisor
        return [{
            'id': self._unique_id(),
            'question_text': f"Divide {dividend} by {divisor}. What is the Quotient and Remainder?",
            'type': 'dual',
            'correct_answer': {'quotient': quotient, 'remainder': remainder},
            'category': 'Division'
        }]

    # --- 5. FACTORS ---
    def generate_factorization(self) -> List[Dict[str, Any]]:
        n = random.randint(10, 499)
        factors = self.prime_factors(n)
        return [{
            'id': self._unique_id(),
            'question_text': f"List all prime factors of {n} (comma separated)",
            'type': 'text',
            'correct_answer': ','.join(map(str, factors)),
            'category': 'Factors'
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

    # --- 6. ALGEBRA ---
    def generate_equation(self) -> List[Dict[str, Any]]:
        a = random.randint(2, 12)
        x = random.randint(-20, 20)
        b = random.randint(-20, 20)
        c = a * x + b
        return [{
            'id': self._unique_id(),
            'question_text': f"Solve for x: {a}x {'+' if b >= 0 else '-'} {abs(b)} = {c}",
            'type': 'single',
            'correct_answer': str(x),
            'category': 'Algebra'
        }]

    # --- 7. FRACTIONS & CONVERSIONS (Clubbed) ---
    def generate_frac2dec(self) -> List[Dict[str, Any]]:
        denom = random.choice(self.friendly_denominators)
        numer = random.randint(1, denom - 1)
        ans = round(numer / denom, 4)
        return [{
            'id': self._unique_id(),
            'question_text': f"Convert {numer}/{denom} to decimal.",
            'type': 'single',
            'correct_answer': ans,
            'category': 'Fractions & Conversions'
        }]

    def generate_dec2perc(self) -> List[Dict[str, Any]]:
        denom = random.choice(self.friendly_denominators)
        numer = random.randint(1, denom - 1)
        dec = round(numer / denom, 4)
        ans = round(dec * 100, 2)
        return [{
            'id': self._unique_id(),
            'question_text': f"Convert {dec} to percentage.",
            'type': 'single',
            'correct_answer': ans,
            'category': 'Fractions & Conversions'
        }]

    def generate_perc2frac(self) -> List[Dict[str, Any]]:
        denom = random.choice(self.friendly_denominators)
        numer = random.randint(1, denom - 1)
        perc = round((numer / denom) * 100, 2)
        ans = self._lowest_terms(numer, denom)
        return [{
            'id': self._unique_id(),
            'question_text': f"Convert {perc}% to fraction (as a/b, lowest terms)",
            'type': 'text',
            'correct_answer': ans,
            'category': 'Fractions & Conversions'
        }]

    # --- 8. GEOMETRY (SVG Fixed) ---
    def generate_geometry(self) -> List[Dict[str, Any]]:
        shape = random.choice(['rectangle', 'circle', 'square'])
        mode = random.choice(['area', 'perimeter'])
        fill_color = "#e3f2fd"
        stroke_color = "#1565c0"
        
        if shape == 'rectangle':
            w = random.randint(5, 15)
            h = random.randint(3, 10)
            if w == h: w += 2
            ans = (w * h) if mode == 'area' else (2 * (w + h))
            
            # FIXED: Corrected {h} r typo and adjusted x coordinate for layout
            svg = f"""
            <div style="display:flex; flex-direction:column; align-items:center;">
                <svg width="240" height="140" viewBox="0 0 240 140">
                    <rect x="25" y="10" width="150" height="80" style="fill:{fill_color};stroke:{stroke_color};stroke-width:3" />
                    <text x="100" y="115" font-family="Arial" font-size="14" text-anchor="middle" font-weight="bold">{w} m</text>
                    <text x="210" y="55" font-family="Arial" font-size="14" text-anchor="middle" font-weight="bold">{h} m</text>
                </svg>
                <div style="margin-top:10px;">Find the <b>{mode.title()}</b>.</div>
            </div>
            """
        elif shape == 'square':
            s = random.randint(4, 12)
            ans = (s * s) if mode == 'area' else (4 * s)
            svg = f"""<div style="display:flex; flex-direction:column; align-items:center;"><svg width="180" height="180" viewBox="0 0 180 180"><rect x="25" y="25" width="100" height="100" style="fill:{fill_color};stroke:{stroke_color};stroke-width:3" /><text x="75" y="150" font-family="Arial" font-size="14" text-anchor="middle" font-weight="bold">{s} m</text></svg><div style="margin-top:10px;">Find the <b>{mode.title()}</b>.</div></div>"""
        else:
            r = random.randint(3, 9)
            ans = round(3.14 * r * r, 2) if mode == 'area' else round(2 * 3.14 * r, 2)
            svg = f"""<div style="display:flex; flex-direction:column; align-items:center;"><svg width="180" height="180" viewBox="0 0 180 180"><circle cx="75" cy="75" r="50" stroke="{stroke_color}" stroke-width="3" fill="{fill_color}" /><line x1="75" y1="75" x2="125" y2="75" style="stroke:#000;stroke-width:2" /><text x="100" y="70" font-family="Arial" font-size="14" text-anchor="middle" font-weight="bold">r = {r} m</text></svg><div style="margin-top:10px;">Find the <b>{mode.title()}</b> (π=3.14).</div></div>"""
        
        return [{
            'id': self._unique_id(),
            'question_text': svg,
            'type': 'single',
            'correct_answer': ans,
            'category': 'Geometry'
        }]

    # --- 9. DATA INTERPRETATION ---
    def generate_data_interpretation(self) -> List[Dict[str, Any]]:
        topic = random.choice(self.scenarios.get('di_topics', [{'title':'Data','labels':['A','B'],'unit':'V'}]))
        labels = topic['labels']
        values = [random.randint(2, 9) * 10 for _ in labels]
        
        q_type = random.choice(['max', 'min', 'total', 'diff'])
        if q_type == 'max':
            ans = labels[values.index(max(values))]; text = f"Which category has the highest {topic['unit']}?"; inp_type = 'text'
        elif q_type == 'min':
            ans = labels[values.index(min(values))]; text = f"Which category has the lowest {topic['unit']}?"; inp_type = 'text'
        elif q_type == 'total':
            text = f"What is the total {topic['unit']}?"; ans = sum(values); inp_type = 'single'
        else:
            text = f"Difference between {labels[0]} and {labels[-1]}?"; ans = abs(values[0] - values[-1]); inp_type = 'single'

        bars_svg = ""
        start_x = 40
        max_val = max(values)
        scale = 100 / max_val if max_val > 0 else 1
        for i, (lbl, val) in enumerate(zip(labels, values)):
            h = val * scale; y = 120 - h; x = start_x + i * 60; color = "#4caf50" if val == max(values) else "#2196f3"
            bars_svg += f"""<rect x="{x}" y="{y}" width="40" height="{h}" fill="{color}" /><text x="{x + 20}" y="135" font-family="Arial" font-size="12" text-anchor="middle">{lbl}</text><text x="{x + 20}" y="{y-5}" font-family="Arial" font-size="12" text-anchor="middle" font-weight="bold">{val}</text>"""
            
        svg = f"""<div style="display:flex; flex-direction:column; align-items:center;"><h5>{topic['title']}</h5><svg width="300" height="150" viewBox="0 0 300 150" style="border-left:2px solid #333; border-bottom:2px solid #333;">{bars_svg}</svg><div style="margin-top:10px;">{text}</div></div>"""
        return [{'id': self._unique_id(), 'question_text': svg, 'type': inp_type, 'correct_answer': ans, 'category': 'Data Interpretation'}]

    # --- 10. LOGICAL REASONING ---
    def generate_logical_reasoning(self) -> List[Dict[str, Any]]:
        mode = random.choice(['series', 'coding'])
        if mode == 'series':
            start = random.randint(1, 10); diff = random.randint(2, 9); seq = [start + i*diff for i in range(5)]; ans = seq[4]
            display_seq = [str(x) for x in seq[:4]] + ["?"]
            text = f"Next in series: <b>{', '.join(display_seq)}</b>"
            return [{'id': self._unique_id(), 'question_text': text, 'type': 'single', 'correct_answer': ans, 'category': 'Logical Reasoning'}]
        else:
            word = random.choice(self.scenarios.get('lr_coding_words', ['APPLE'])); shift = random.choice([1, -1])
            def shift_char(c, k): return chr(((ord(c) - 65 + k) % 26) + 65)
            coded = "".join([shift_char(c, shift) for c in word])
            target = random.choice([w for w in self.scenarios.get('lr_coding_words', ['TIGER']) if w != word])
            target_coded = "".join([shift_char(c, shift) for c in target])
            text = f"If <b>{word}</b> is <b>{coded}</b>, what is <b>{target}</b>?"
            return [{'id': self._unique_id(), 'question_text': text, 'type': 'text', 'correct_answer': target_coded, 'category': 'Logical Reasoning'}]

    # --- 11. DATA SUFFICIENCY ---
    def generate_data_sufficiency(self) -> List[Dict[str, Any]]:
        problem = random.choice(self.scenarios.get('ds_problems', [{'question':'?', 'stat1':'A', 'stat2':'B', 'correct':'Both'}]))
        raw_correct = problem.get('correct', 'Both')
        if "Both" in raw_correct: correct_key = "Both"
        elif "Only I" in raw_correct: correct_key = "Only I"
        elif "Only II" in raw_correct: correct_key = "Only II"
        else: correct_key = "Neither"

        html = f"""
        <div class="text-start">
            <p class="fs-5 fw-bold mb-3">{problem['question']}</p>
            <div class="card mb-3 bg-light border-0"><div class="card-body">
                <p class="mb-2"><strong>I:</strong> {problem['stat1']}</p><p class="mb-0"><strong>II:</strong> {problem['stat2']}</p>
            </div></div>
            <div class="alert alert-primary py-2 px-3 small"><strong>Type one:</strong> "Only I", "Only II", "Both", "Neither"</div>
        </div>"""
        return [{'id': self._unique_id(), 'question_text': html, 'type': 'text', 'correct_answer': correct_key, 'category': 'Data Sufficiency'}]

    # --- 12. PROFIT AND LOSS ---
    def generate_profit_loss(self) -> List[Dict[str, Any]]:
        item = random.choice(self.scenarios['profit_loss_items']); name = random.choice(self.scenarios['profit_loss_names'])
        q_type = random.choice(['amount', 'percent']); cp = random.randint(5, 50) * 10; is_profit = random.choice([True, False])
        if q_type == 'amount':
            val = random.randint(1, 10) * 5; sp = (cp + val) if is_profit else (cp - val)
            text = f"{name} bought {item} for ${cp} and sold for ${sp}. What is the {'Profit' if is_profit else 'Loss'}?"; ans = val
        else:
            perc = random.choice([10, 20, 25, 50]); sp = (cp + (cp * perc // 100)) if is_profit else (cp - (cp * perc // 100))
            text = f"CP = ${cp}, SP = ${sp}. Find {'Profit' if is_profit else 'Loss'} %?"; ans = perc
        return [{'id': self._unique_id(), 'question_text': text, 'type': 'single', 'correct_answer': ans, 'category': 'Profit & Loss'}]

    # --- 13. UNITARY METHOD ---
    def generate_unitary_method(self) -> List[Dict[str, Any]]:
        if random.choice(['cost', 'work']) == 'cost':
            group, count = random.choice([('dozen', 12), ('score', 20), ('pack of 10', 10)])
            item = random.choice(self.scenarios['unitary_cost_items']); unit = random.randint(2, 9); total = unit * count; target = random.choice([2, 3, 5])
            text = f"If 1 {group} {item} costs ${total}, cost of {target}?"; ans = target * unit
        else:
            scen = random.choice(self.scenarios['unitary_work_scenarios']); w1 = random.choice([5, 10, 15]); d1 = random.choice([6, 12, 20]); effort = w1 * d1
            possible_w2 = [w for w in range(2, effort) if effort % w == 0 and w != w1]
            if not possible_w2: return self.generate_unitary_method()
            w2 = random.choice(possible_w2); text = f"If {w1} {scen['actor']} can {scen['task']} in {d1} days, days for {w2}?"; ans = effort // w2
        return [{'id': self._unique_id(), 'question_text': text, 'type': 'single', 'correct_answer': ans, 'category': 'Unitary Method'}]

    def generate_all(self) -> List[Dict[str, Any]]:
        segments = []
        for _ in range(2): segments.extend(self.generate_addition())
        for _ in range(2): segments.extend(self.generate_subtraction())
        for _ in range(2): segments.extend(self.generate_multiplication())
        for _ in range(2): segments.extend(self.generate_division())
        for _ in range(2): segments.extend(self.generate_factorization())
        for _ in range(2): segments.extend(self.generate_equation())
        for _ in range(2): segments.extend(self.generate_frac2dec())
        for _ in range(2): segments.extend(self.generate_dec2perc())
        for _ in range(2): segments.extend(self.generate_perc2frac())
        for _ in range(2): segments.extend(self.generate_geometry())
        for _ in range(2): segments.extend(self.generate_data_interpretation())
        for _ in range(2): segments.extend(self.generate_logical_reasoning())
        for _ in range(2): segments.extend(self.generate_data_sufficiency())
        for _ in range(2): segments.extend(self.generate_profit_loss())
        for _ in range(2): segments.extend(self.generate_unitary_method())
        random.shuffle(segments)
        return segments