from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class AddStockForm(FlaskForm):
    stock_symbol = StringField('Stock Symbol', validators=[DataRequired(), Length(max=10)])
    submit = SubmitField('Add to Watchlist')

class ScannerForm(FlaskForm):
    scanner_type = SelectField('Select Scanner', choices=[
        ('high_relative_volume', 'High Relative Volume'),
        ('momentum', 'Momentum Scanner'),
        ('macd', 'MACD Scanner'),
        ('rsi', 'RSI Scanner')
    ], validators=[DataRequired()])
    submit = SubmitField('Run Scanner')
