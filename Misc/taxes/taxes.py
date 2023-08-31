from json import load, dump
from os import path
from locale import setlocale, LC_MONETARY, currency


def to_curr(x):
    setlocale(LC_MONETARY, 'en_IN')
    result = currency(x, grouping=True)
    return f'{result[: result.rfind(".")]:<11}'


class TaxBrackets:
    def __init__(self, file_path):
        self.file_path = file_path
        self.tax_brackets = []
        self.load()
        if not self.tax_brackets:
            self.read()
        self.save()

    def load(self):
        with open(self.file_path, 'r', encoding='utf-8') as f:
            data = load(f)
        if 'tax_brackets' not in data:
            self.tax_brackets = None
        else:
            self.tax_brackets = data['tax_brackets']

    def read(self):
        self.tax_brackets = []
        while (line := input('low (Rs.), high (Rs.), tax %: ')):
            try:
                low, high, tax = line.split()
                low = int(low)
                high = float(high) if high == 'inf' else int(high)
                tax = int(tax)
                if not (0 <= tax <= 100):
                    raise ValueError
                self.tax_brackets.append((low, high, tax))
            except ValueError as _:
                print(f'Invalid input!')

    def save(self):
        with open(self.file_path, 'w', encoding='utf-8') as f:
            data = {'tax_brackets': self.tax_brackets}
            dump(data, f, indent=2)

    def print_tax(self, low, high, tax):
        low, high, tax = list(map(to_curr, [low, high, tax]))
        print(f'\tFor {low} to {high}: {tax}')

    def calculate_tax(self, income):
        total_tax = 0
        for bracket in self.tax_brackets:
            low, high, tax = bracket
            if income < high:
                tax_amount = ((income - low) // 100) * tax
                total_tax += tax_amount
                self.print_tax(low, income, tax_amount)
                break
            tax_amount = ((high - low) // 100) * tax
            total_tax += tax_amount
            self.print_tax(low, high, tax_amount)
        return total_tax


def main():
    file_path = path.join('.', 'taxes.json')
    tb = TaxBrackets(file_path)
    income = int(input('Income: '))
    tax = tb.calculate_tax(income)
    print(f'Tax for {to_curr(income)}: {to_curr(tax)}')


if __name__ == '__main__':
    main()
