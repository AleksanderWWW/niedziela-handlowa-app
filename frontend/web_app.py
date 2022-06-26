from flask import Flask, redirect, url_for, render_template, session
from flask_wtf import FlaskForm
from wtforms.fields import DateField
from wtforms.validators import DataRequired
from wtforms import validators, SubmitField


_APP = Flask(__name__)


class InfoForm(FlaskForm):
    submit = SubmitField('Submit')
    date_field = DateField('Date', format='%Y-%m-%d', validators=(validators.DataRequired(),))


class WebApp:
    def __init__(self, data_loader, data_parser) -> None:
        self.loader = data_loader
        self.parser = data_parser
        
        global _APP
        _APP.config['SECRET_KEY'] = '#$%^&*'
    
    @_APP.route('/', methods=['GET','POST'])
    def index():
        form = InfoForm()
        if form.validate_on_submit():
            session['date'] = form.date_field.data
            return redirect('date')
        return render_template('index.html', form=form)

    @_APP.route('/date', methods=['GET','POST'])
    def date():
        return render_template('date.html')

    def run(self):
        _APP.run(debug=True)