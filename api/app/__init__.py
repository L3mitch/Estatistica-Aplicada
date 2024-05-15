from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)

from app import routes