from flask import Flask, render_template, request, redirect, url_for, session
from tax_calculator import TaxCalculator

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a real secret key for session management

@app.route('/')
def entry():
    return render_template('entry.html')

@app.route('/save_user_data', methods=['POST'])
def save_user_data():
    session['user_data'] = {
        'name': request.form.get('name'),
        'age': int(request.form.get('age')),
        'gender': request.form.get('gender')
    }
    return redirect(url_for('salary_income'))

@app.route('/salary_income', methods=['GET', 'POST'])
def salary_income():
    if request.method == 'POST':
        session['salary_income_data'] = {
            'basic_salary': float(request.form.get('basic_salary', 0)),
            'hra': float(request.form.get('hra', 0)),
            'special_allowance': float(request.form.get('special_allowance', 0)),
            'other_allowances': float(request.form.get('other_allowances', 0))
        }
        return redirect(url_for('house_property'))
    return render_template('salary_income.html')

@app.route('/house_property', methods=['GET', 'POST'])
def house_property():
    if request.method == 'POST':
        session['house_property_data'] = {
            'value_of_property': float(request.form.get('value_of_property', 0)),
            'rental_income': float(request.form.get('rental_income', 0)),
            'municipal_taxes': float(request.form.get('municipal_taxes', 0)),
            'home_loan_interest': float(request.form.get('home_loan_interest', 0))
        }
        return redirect(url_for('other_sources'))
    return render_template('house_property.html')

@app.route('/other_sources', methods=['GET', 'POST'])
def other_sources():
    if request.method == 'POST':
        session['other_sources_data'] = {
            'interest_income': float(request.form.get('interest_income', 0)),
            'dividend_income': float(request.form.get('dividend_income', 0)),
            'rental_income': float(request.form.get('rental_income', 0)),
            'other_income': float(request.form.get('other_income', 0))
        }
        return redirect(url_for('income_business_profession'))
    return render_template('other_sources.html')

@app.route('/income_business_profession', methods=['GET', 'POST'])
def income_business_profession():
    if request.method == 'POST':
        session['business_profession_data'] = {
            'business_income': float(request.form.get('business_income', 0)),
            'profession_income': float(request.form.get('profession_income', 0)),
            'other_business_income': float(request.form.get('other_business_income', 0))
        }
        return redirect(url_for('capital_gains'))
    return render_template('income_business_profession.html')

@app.route('/capital_gains', methods=['GET', 'POST'])
def capital_gains():
    if request.method == 'POST':
        session['capital_gains_data'] = {
            'short_term_gains': float(request.form.get('short_term_gains', 0)),
            'long_term_gains': float(request.form.get('long_term_gains', 0)),
            'other_capital_gains': float(request.form.get('other_capital_gains', 0))
        }
        return redirect(url_for('deductions_exemptions'))
    return render_template('capital_gains.html')

@app.route('/deductions_exemptions', methods=['GET', 'POST'])
def deductions_exemptions():
    if request.method == 'POST':
        session['deductions_exemptions_data'] = {
            'section_80c': float(request.form.get('section_80c', 0)),
            'section_80d': float(request.form.get('section_80d', 0)),
            'section_24': float(request.form.get('section_24', 0)),
            'other_exemptions': float(request.form.get('other_exemptions', 0))
        }
        return redirect(url_for('summary'))
    return render_template('deductions_exemptions.html')

@app.route('/summary')
def summary():
    calculator = TaxCalculator()
    
    # Set user data
    user_data = session.get('user_data', {})
    calculator.set_personal_info(user_data.get('name', ''), user_data.get('age', 0), user_data.get('financial_year', ''))
    
    # Set all income and deduction data
    calculator.set_salary_income(session.get('salary_income_data', {}))
    calculator.set_house_property_income(session.get('house_property_data', {}))
    calculator.set_other_income(session.get('other_sources_data', {}))
    calculator.set_business_income(session.get('business_profession_data', {}))
    calculator.set_capital_gains(session.get('capital_gains_data', {}))
    calculator.set_deductions(session.get('deductions_exemptions_data', {}))
    
    # Calculate tax
    calculator.calculate_taxable_income()
    calculator.calculate_tax()
    
    summary_data = calculator.get_summary()
    
    return render_template('summary.html', summary=summary_data)

@app.route('/generate_report', methods=['POST'])
def generate_report():
    # Implement report generation logic here
    return "Report generated successfully!"

if __name__ == '__main__':
    app.run(debug=True)