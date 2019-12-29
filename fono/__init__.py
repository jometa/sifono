import os
import json
from flask import Flask, render_template, jsonify, redirect, url_for
from flask_cors import CORS
from environs import Env

def create_app():
    app = Flask(__name__, instance_relative_config=True, static_url_path="")
    app.config.from_mapping(
        SECRET_KEY=APP_SECRET
    )