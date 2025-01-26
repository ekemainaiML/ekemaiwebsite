from flask import render_template, request, Blueprint, flash, redirect, url_for, session
from utils.utility import get_all_aiagents
from flask import render_template, Blueprint

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')


@views.route('/about')
def about():
    return render_template('about.html')


@views.route('/pricing')
def pricing():
    return render_template('pricing.html')


@views.route('/digitaltemp', methods=['GET', 'POST'])
async def digitaltemp():
    products = await get_all_aiagents()
    if request.method == 'GET':
        return render_template('digitaltemp.html', products=products)
    return render_template('digitaltemp.html')
