# -*- coding: utf-8 -*-

from flask import Blueprint, g, render_template

index = Blueprint('home', __name__)


@index.route('/')
def get_index():
    return render_template('index.html')