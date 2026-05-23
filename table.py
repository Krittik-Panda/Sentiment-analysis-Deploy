from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from datetime import datetime

db = SQLAlchemy()

class Prediction(db.Model):
    __tablename__ = 'prediction'
    id = db.Column(db.Integer, primary_key = True)
    text = db.Column(db.String(1000), nullable = False)
    label = db.Column(db.String(50) , nullable = True)
    pos_proba = db.Column(db.Float, nullable = True )
    neg_proba = db.Column(db.Float, nullable = True )
    created_at = db.Column(db.DateTime, default=datetime.utcnow())

