from flask import Flask, redirect, render_template, session
from flask_wtf import FlaskForm
from wtforms.fields import DateField
from wtforms import validators, SubmitField


APP = Flask(__name__)
APP.config['SECRET_KEY'] = '#$%^&*'


class InfoForm(FlaskForm):
    submit = SubmitField('Submit')
    date_field = DateField('Date', format='%Y-%m-%d', validators=(validators.DataRequired(),))


""" class WebApp(FlaskView):
    default_methods = ['GET', 'POST']

    def __init__(self, backend_interface) -> None:
        self.backend_interface = backend_interface

    def home_view(self):
        form = InfoForm()
        if form.validate_on_submit():
            chosen_date = form.date_field.data
            year = chosen_date.year
            breakpoint()
            self.backend_interface.load_data(year, force_on_error=True)
            self.backend_interface.extract_dates()
            print(self.backend_interface.dates)
            session['date'] = form.date_field.data

            return redirect('results')
        return render_template('index.html', form=form)

    def results(self):
        return render_template('date.html')

    def run(self):
        APP.run(debug=True) """


class BackendWrapper:
    def __init__(self) -> None:
        self.backend = None

    def set_backend(self, backend):
        self.backend = backend

wrapper = BackendWrapper()


class WebApp:
    def __init__(self, backend_inter) -> None:
        global wrapper
        wrapper.set_backend(backend_inter)
        self.app = APP

    @APP.route("/", methods=["GET", "POST"])
    def index():
        form = InfoForm()
        if form.validate_on_submit():
            chosen_date = form.date_field.data
            year = chosen_date.year
            day = chosen_date.day
            month = chosen_date.month

            wrapper.backend.load_data(year, force_on_error=True)
            wrapper.backend.extract_dates()
            if wrapper.backend.check_if_date_work_free(day, month, year):
                session["is_trade_free"] = "Obowiązuje zakaz handlu"
            else:
                session["is_trade_free"] = "Jest to dzień handlowy"
            session['date'] = form.date_field.data

            return redirect('date')
        return render_template('index.html', form=form)

    @APP.route("/date", methods=["GET", "POST"])
    def date():
        return render_template("date.html")

    def run(self):
        APP.run(debug=True)
