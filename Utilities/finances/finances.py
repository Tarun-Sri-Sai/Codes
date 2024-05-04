import argparse
import pandas
import decimal
import sys


class InputParser:
    def __init__(self):
        self._args = None
        self._parser = None
        self._subparsers = None
        self._incometax_parser = None
        self._rdeposit_parser = None
        self._fdeposit_parser = None

    @property
    def parser(self):
        if self._parser is not None:
            return self._parser

        self._parser = argparse.ArgumentParser(
            description='Finance calculator')
        return self._parser

    @property
    def subparsers(self):
        if self._subparsers is not None:
            return self._subparsers

        self._subparsers = self.parser.add_subparsers(
            title='subcommands', dest='subcommand')
        return self._subparsers

    def add_incometax_parser(self):
        if self._incometax_parser is not None:
            return

        self._incometax_parser = self.subparsers.add_parser(
            'incometax',
            help='Calculate the income tax')
        self._incometax_parser.add_argument(
            'income', type=float,
            help='Income to calculate tax for')
        self._incometax_parser.add_argument(
            'tax_brackets', type=str,
            help='Path to CSV file containing tax brackets')

    def add_rdeposit_parser(self):
        if self._rdeposit_parser is not None:
            return

        self._rdeposit_parser = self.subparsers.add_parser(
            'rdeposit',
            help='Calculate the recurring deposit')
        self._rdeposit_parser.add_argument(
            'amount', type=float,
            help='Monthly contribution amount')
        self._rdeposit_parser.add_argument(
            'interest', type=float,
            help='Interest rate p.a.')
        self._rdeposit_parser.add_argument(
            'period', type=int,
            help='Calculation period in months')

    def add_fdeposit_parser(self):
        if self._fdeposit_parser is not None:
            return

        self._fdeposit_parser = self.subparsers.add_parser(
            'fdeposit',
            help='Calculate the fixed deposit')
        self._fdeposit_parser.add_argument(
            'principal', type=float,
            help='Principal amount')
        self._fdeposit_parser.add_argument(
            'interest', type=float,
            help='Interest rate p.a.')
        self._fdeposit_parser.add_argument(
            'period', type=int,
            help='Calculation period in months')

    @property
    def args(self):
        if self._args is not None:
            return self._args

        return vars(self.parser.parse_args())


class IncomeTax:
    def __init__(self):
        self._tax_brackets = None

    def set_tax_brackets(self, tax_brackets_file: str):
        data = pandas.read_csv(tax_brackets_file)
        self._tax_brackets = [(
            decimal.Decimal(row['lower_limit_pa']),
            decimal.Decimal(row['upper_limit_pa']),
            decimal.Decimal(row['income_tax_percent'])
        ) for _, row in data.iterrows()]

    def calculate(self, income_pa):
        result = decimal.Decimal(0)

        for (lower_limit_pa,
             upper_limit_pa,
             income_tax_percent) in self._tax_brackets:
            lower_limit_pa = decimal.Decimal(lower_limit_pa)
            upper_limit_pa = decimal.Decimal(upper_limit_pa)
            income_tax_percent = decimal.Decimal(income_tax_percent)

            if decimal.Decimal(income_pa) < upper_limit_pa:
                result += ((decimal.Decimal(income_pa) - lower_limit_pa)
                           * income_tax_percent)
                return result / decimal.Decimal(100)
            result += ((upper_limit_pa - lower_limit_pa) * income_tax_percent)
        return result / decimal.Decimal(100)


class RDeposit:
    def calculate_interest(self, monthly_contribution, annual_interest_rate,
                           num_months):
        decimal.getcontext().prec = 28
        monthly_interest_rate = (decimal.Decimal(annual_interest_rate)
                                 / decimal.Decimal(12 * 100))
        total_amount = decimal.Decimal(0)
        total_interest = decimal.Decimal(0)
        for _ in range(1, num_months + 1):
            total_amount += decimal.Decimal(monthly_contribution)
            interest_this_month = total_amount * monthly_interest_rate
            total_interest += interest_this_month
            total_amount += interest_this_month
        return total_interest


class FDeposit:
    def calculate_interest(self, principal, annual_interest_rate, num_months):
        decimal.getcontext().prec = 28
        monthly_interest_rate = (decimal.Decimal(annual_interest_rate)
                                 / decimal.Decimal(12 * 100))
        total_amount = decimal.Decimal(principal)
        total_interest = decimal.Decimal(0)
        for _ in range(1, num_months + 1):
            interest_this_month = total_amount * monthly_interest_rate
            total_interest += interest_this_month
            total_amount += interest_this_month
        return total_interest


def get_income_tax(args):
    income_tax = IncomeTax()
    income_tax.set_tax_brackets(args['tax_brackets'])
    result = income_tax.calculate(args['income'])
    return f'{result:.2f}'


def get_rdeposit(args):
    r_deposit = RDeposit()
    result = r_deposit.calculate_interest(
        args['amount'], args['interest'], args['period'])
    return f'{result:.2f}'


def get_fdeposit(args):
    f_deposit = FDeposit()
    result = f_deposit.calculate_interest(
        args['principal'], args['interest'], args['period'])
    return f'{result:.2f}'


def main():
    input_parser = InputParser()
    input_parser.add_incometax_parser()
    input_parser.add_rdeposit_parser()
    input_parser.add_fdeposit_parser()
    args = input_parser.args

    subcommands = {
        'incometax': get_income_tax,
        'rdeposit': get_rdeposit,
        'fdeposit': get_fdeposit
    }
    try:
        method = subcommands[args['subcommand']]
    except KeyError:
        print(input_parser.parser.print_help())
        sys.exit(1)
    result = method(args)
    print(result)


if __name__ == '__main__':
    main()
