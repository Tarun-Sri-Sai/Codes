from argparse import ArgumentParser
from pandas import read_csv
from locale import setlocale, LC_ALL, currency


setlocale(LC_ALL, 'en-IN')


class IncomeTax:
    def __init__(self, tax_brackets_file: str):
        self.__tax_brackets = None

        self.__get_tax_brackets(tax_brackets_file)

    def __get_tax_brackets(self, tax_brackets_file: str):
        self.__tax_brackets = []
        data = read_csv(tax_brackets_file)
        for _, row in data.iterrows():
            self.__tax_brackets.append((
                float(row['lower_limit_pa']),
                float(row['upper_limit_pa']),
                float(row['income_tax_percent'])
            ))

    def calculate(self, income_pa: float) -> int:
        result = 0

        for (lower_limit_pa,
             upper_limit_pa,
             income_tax_percent) in self.__tax_brackets:
            if income_pa < upper_limit_pa:
                result += ((income_pa - lower_limit_pa) 
                           * income_tax_percent)
                return result // 100
            result += ((upper_limit_pa - lower_limit_pa) 
                       * income_tax_percent)
        return result // 100


def parse_arguments():
    parser = ArgumentParser()
    parser.add_argument('--tax-brackets-file', '-t', 
                        dest='tax_brackets_file', type=str)
    parser.add_argument('--income', '-i', 
                        dest='income', type=float)

    args = parser.parse_args()
    
    if not (args.tax_brackets_file and args.income):
        parser.print_help()
        exit()
    
    return {
        'tax_brackets_file': args.tax_brackets_file,
        'income': args.income
    }


def format_currency(value: int) -> str:
    return currency(value, grouping=True)


def main():
    arguments = parse_arguments()
    income_tax = IncomeTax(arguments['tax_brackets_file'])
    formatted_string = format_currency(
        income_tax.calculate(arguments['income']))
    print(formatted_string)


if __name__ == '__main__':
    main()
