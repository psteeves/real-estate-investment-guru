import numpy as np

_MORTGAGE_PREMIUM_SCALE = {0.05: 0.04, 0.1: 0.031, 0.15: 0.028, 0.2: 0}


class TrivialFinancialModel:
    def __call__(self, input_):
        return 1.0


class SimpleFinancialModel:
    def __init__(
        self,
        downpayment: float,
        closing_fees: float,
        interest_rate: float,
        amortization: int,
        forecast_horizon: int,
        vacancy: float,
        property_tax_rate: float,
        rate_rent_increase: float,
        expense_ratio: float,
        yearly_reserves: int,
    ):
        self._downpayment = downpayment
        self._closing_fees = closing_fees
        self._interest_rate = interest_rate
        self._amortization = amortization
        self._vacancy = vacancy
        self._rate_rent_increase = rate_rent_increase
        self._expense_ratio = expense_ratio
        self._yearly_savings = yearly_reserves

        self._mortgage_premium = _MORTGAGE_PREMIUM_SCALE.get(self._downpayment)
        if self._mortgage_premium is None:
            raise ValueError(
                f"Downpayment must be one of {list(_MORTGAGE_PREMIUM_SCALE.keys())}. Got `{self._downpayment}`"
            )

        self._forecast_horizon = forecast_horizon
        # TODO automatically lookup property tax rate by city.
        self._property_tax = property_tax_rate
        # TODO do something smarter for income tax rate.
        self._income_tax_rate = 0.3

    def _forecast_gross_revenue(self, monthly_rent):
        # Income
        gross_rent_income = np.array(
            [
                monthly_rent
                * 12
                * (1 - self._vacancy)
                * (1 + self._rate_rent_increase) ** i
                for i in range(self._forecast_horizon)
            ]
        )
        return gross_rent_income

    def _predict(self, prop):
        price = prop["Price"]
        monthly_rent = prop["Predicted Rent Revenue"]

        downpayment = price * self._downpayment
        closing_fees = self._closing_fees * price
        total_investment = downpayment + closing_fees

        loan_principal = (1 + self._mortgage_premium) * price - downpayment

        # Multiply expense ratio by 1.5 for older properties
        property_expense_ratio = (
            self._expense_ratio if prop.year_built > 2010 else self._expense_ratio * 1.5
        )

        yearly_gross_revenue = self._forecast_gross_revenue(monthly_rent)

        # Expenses
        expenses = property_expense_ratio * yearly_gross_revenue
        interest_payments = np.ipmt(
            rate=self._interest_rate,
            per=[i + 1 for i in range(self._forecast_horizon)],
            nper=self._amortization,
            pv=-loan_principal,
        )
        property_taxes = np.array([self._property_tax * price] * self._forecast_horizon)

        # Tax
        taxable_income = (
            yearly_gross_revenue - expenses - interest_payments - property_taxes
        )
        income_tax = np.clip(self._income_tax_rate * taxable_income, 0, None)
        net_income = taxable_income - income_tax

        principal_repayments = np.ppmt(
            rate=self._interest_rate,
            per=[i + 1 for i in range(self._forecast_horizon)],
            nper=self._amortization,
            pv=-loan_principal,
        )
        yearly_reserves = [self._yearly_savings] * self._forecast_horizon

        net_cash_flow = net_income - principal_repayments - yearly_reserves
        net_equity = net_cash_flow + principal_repayments

        cap_rate = (yearly_gross_revenue - property_taxes - expenses) / price
        cash_on_cash_return = net_cash_flow / total_investment
        return_on_equity = net_equity / total_investment

        mortg_premium = self._mortgage_premium * price

        return (
            total_investment,
            mortg_premium,
            yearly_gross_revenue.mean(),
            net_income.mean(),
            net_cash_flow.mean(),
            cash_on_cash_return.mean(),
            return_on_equity.mean(),
            cap_rate.mean(),
        )

    def predict(self, properties):
        properties[
            [
                "Initial Investment",
                "Mrtg. Premium",
                "Gross Revenue",
                "Net Income",
                "Net Cash",
                "Cash Return",
                "ROE",
                "Cap Rate",
            ]
        ] = properties.apply(self._predict, axis=1, result_type="expand")
        return properties
