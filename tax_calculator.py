class TaxCalculator:
    def __init__(self):
        self.name = ""
        self.age = 0
        self.financial_year = ""
        self.salary_income = 0
        self.house_property_income = 0
        self.other_income = 0
        self.business_income = 0
        self.capital_gains = 0
        self.deductions = 0
        self.taxable_income = 0
        self.tax = 0

    def set_personal_info(self, name, age, financial_year):
        self.name = name
        self.age = age
        self.financial_year = financial_year

    def set_salary_income(self, data):
        self.salary_income = sum(data.values())

    def set_house_property_income(self, data):
        rental_income = float(data.get('rental_income', 0))
        municipal_taxes = float(data.get('municipal_taxes', 0))
        home_loan_interest = float(data.get('home_loan_interest', 0))
        
        net_annual_value = rental_income - municipal_taxes
        self.house_property_income = max(0, net_annual_value - home_loan_interest)

    def set_other_income(self, data):
        self.other_income = sum(float(value) for value in data.values())

    def set_business_income(self, data):
        self.business_income = sum(float(value) for value in data.values())

    def set_capital_gains(self, data):
        self.capital_gains = sum(float(value) for value in data.values())

    def set_deductions(self, data):
        self.deductions = sum(float(value) for value in data.values())

    def calculate_taxable_income(self):
        self.total_income = (self.salary_income + self.house_property_income + 
                             self.other_income + self.business_income + self.capital_gains)
        self.taxable_income = max(0, self.total_income - self.deductions)

    def calculate_tax(self):
        if self.taxable_income <= 250000:
            self.tax = 0
        elif self.taxable_income <= 500000:
            self.tax = (self.taxable_income - 250000) * 0.05
        elif self.taxable_income <= 1000000:
            self.tax = 12500 + (self.taxable_income - 500000) * 0.2
        else:
            self.tax = 112500 + (self.taxable_income - 1000000) * 0.3

        # Apply surcharge if applicable
        if self.taxable_income > 5000000:
            surcharge_rate = 0.10 if self.taxable_income <= 10000000 else 0.15
            surcharge = self.tax * surcharge_rate
            self.tax += surcharge

        # Add Health and Education Cess
        self.tax += self.tax * 0.04

    def get_summary(self):
        return {
            'name': self.name,
            'age': self.age,
            'financial_year': self.financial_year,
            'salary_income': self.salary_income,
            'house_property_income': self.house_property_income,
            'other_income': self.other_income,
            'business_income': self.business_income,
            'capital_gains': self.capital_gains,
            'total_income': self.total_income,
            'deductions': self.deductions,
            'taxable_income': self.taxable_income,
            'tax': self.tax
        }

# The run() method is removed as it's not needed for the web application