from flask import Flask, render_template, redirect, url_for, flash, request
from config import Config
from forms import RegistrationForm, LoginForm, AddStockForm, ScannerForm
from models import db, User, Watchlist, StockData, Alert
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from ml_models import predict_price
from news_sentiment import get_news_sentiment
from portfolio import simple_portfolio_summary
import yfinance as yf

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
@login_required
def index():
    watchlist = Watchlist.query.filter_by(user_id=current_user.id).all()
    return render_template('index.html', watchlist=watchlist)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful, please login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('index'))
        flash('Invalid credentials', 'danger')
    return render_template('login.html', form=form)

@app.route('/stock/<symbol>')
@login_required
def stock_detail(symbol):
    predicted_price = predict_price(symbol)
    sentiment = get_news_sentiment(symbol)
    stock = yf.Ticker(symbol)
    hist = stock.history(period='1y')
    return render_template('stock_detail.html', symbol=symbol, hist=hist, predicted_price=predicted_price, sentiment=sentiment)

@app.route('/scanners', methods=['GET', 'POST'])
@login_required
def scanners():
    form = ScannerForm()
    if form.validate_on_submit():
        results = run_scanner(form.scanner_type.data)
        return render_template('scanner_results.html', results=results)
    return render_template('scanners.html', form=form)

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        db.session.commit()
        flash('Profile updated successfully.', 'success')
        return redirect(url_for('profile'))
    return render_template('profile.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/portfolio', methods=['GET'])
@login_required
def portfolio_summary():
    stocks = ['AAPL', 'MSFT', 'GOOGL']  # Example stocks, replace with user's watchlist
    summary = simple_portfolio_summary(stocks)
    return render_template('portfolio.html', summary=summary)
