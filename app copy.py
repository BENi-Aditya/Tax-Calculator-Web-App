from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a real secret key for session management

@app.route('/')
def entry():
    return render_template('entry.html')

@app.route('/save_user_data', methods=['POST'])
def save_user_data():
    user_data = {
        'name': request.form.get('name'),
        'age': request.form.get('age'),
        'gender': request.form.get('gender')
    }
    session['user_data'] = user_data
    return redirect(url_for('salary_income'))

@app.route('/salary_income', methods=['GET', 'POST'])
def salary_income():
    if request.method == 'POST':
        salary_income_data = {
            'basic_salary': float(request.form.get('basic_salary', 0)),
            'hra': float(request.form.get('hra', 0)),
            'special_allowance': float(request.form.get('special_allowance', 0)),
            'other_income': float(request.form.get('other_income', 0))
        }
        session['salary_income_data'] = salary_income_data
        return redirect(url_for('income_house_property'))
    return render_template('salary_income.html')

@app.route('/income_house_property', methods=['GET', 'POST'])
def house_property():
    if request.method == 'POST':
        house_property_data = {
            'rental_income': float(request.form.get('rental_income', 0)),
            'property_tax': float(request.form.get('property_tax', 0))
        }
        session['house_property_data'] = house_property_data
        return redirect(url_for('income_other_sources'))
    return render_template('income_house_property.html')

@app.route('/income_other_sources', methods=['GET', 'POST'])
def income_other_sources():
    if request.method == 'POST':
        other_sources_data = {
            'interest_income': float(request.form.get('interest_income', 0)),
            'dividend_income': float(request.form.get('dividend_income', 0))
        }
        session['other_sources_data'] = other_sources_data
        return redirect(url_for('income_business_profession'))
    return render_template('income_other_sources.html')

@app.route('/income_business_profession', methods=['GET', 'POST'])
def income_business_profession():
    if request.method == 'POST':
        business_profession_data = {
            'business_income': float(request.form.get('business_income', 0)),
            'profession_income': float(request.form.get('profession_income', 0))
        }
        session['business_profession_data'] = business_profession_data
        return redirect(url_for('capital_gains'))
    return render_template('income_business_profession.html')

@app.route('/capital_gains', methods=['GET', 'POST'])
def capital_gains():
    if request.method == 'POST':
        capital_gains_data = {
            'short_term_capital_gains': float(request.form.get('short_term_capital_gains', 0)),
            'long_term_capital_gains': float(request.form.get('long_term_capital_gains', 0))
        }
        session['capital_gains_data'] = capital_gains_data
        return redirect(url_for('deductions_exemptions'))
    return render_template('capital_gains.html')

@app.route('/deductions_exemptions', methods=['GET', 'POST'])
def deductions_exemptions():
    if request.method == 'POST':
        deductions_exemptions_data = {
            'section_80c': float(request.form.get('section_80c', 0)),
            'section_80d': float(request.form.get('section_80d', 0)),
            'section_24b': float(request.form.get('section_24b', 0))
        }
        session['deductions_exemptions_data'] = deductions_exemptions_data
        return redirect(url_for('summary'))
    return render_template('deductions_exemptions.html')

@app.route('/summary')
def summary():
    user_data = session.get('user_data', {})
    salary_income_data = session.get('salary_income_data', {})
    house_property_data = session.get('house_property_data', {})
    other_sources_data = session.get('other_sources_data', {})
    business_profession_data = session.get('business_profession_data', {})
    capital_gains_data = session.get('capital_gains_data', {})
    deductions_exemptions_data = session.get('deductions_exemptions_data', {})

    # Calculate taxable income and tax here based on collected data
    taxable_income = (
        salary_income_data.get('basic_salary', 0) +
        salary_income_data.get('hra', 0) +
        salary_income_data.get('special_allowance', 0) +
        salary_income_data.get('other_income', 0) +
        house_property_data.get('rental_income', 0) +
        other_sources_data.get('interest_income', 0) +
        other_sources_data.get('dividend_income', 0) +
        business_profession_data.get('business_income', 0) +
        business_profession_data.get('profession_income', 0) +
        capital_gains_data.get('short_term_capital_gains', 0) +
        capital_gains_data.get('long_term_capital_gains', 0)
    )

    # Example calculation (to be adjusted as needed)
    tax = taxable_income * 0.1  # Example tax calculation (10% of taxable income)

    return render_template('summary.html',
                           user_data=user_data,
                           salary_income_data=salary_income_data,
                           house_property_data=house_property_data,
                           other_sources_data=other_sources_data,
                           business_profession_data=business_profession_data,
                           capital_gains_data=capital_gains_data,
                           deductions_exemptions_data=deductions_exemptions_data,
                           taxable_income=taxable_income,
                           tax=tax)

if __name__ == '__main__':
    app.run(debug=True)
