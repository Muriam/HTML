from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import create_engine
from wtforms import SubmitField, RadioField, StringField
from flask_wtf import FlaskForm
import os
from wtforms.validators import DataRequired, Optional


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dataBase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
migrate = Migrate(app, db)
engine = create_engine('sqlite:///dataBase.db')
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY


class Kingdom(db.Model):
    __tablename__ = 'kingdom'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
    with_species = db.relationship('Species', backref='kingdom')


class DivisionOrPhylum(db.Model):
    __tablename__ = 'divisionOrPhylum'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
    with_species = db.relationship('Species', backref='divisionOrPhylum')


class Class(db.Model):
    __tablename__ = 'class'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
    with_species = db.relationship('Species', backref='class')


class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
    with_species = db.relationship('Species', backref='order')


class Family(db.Model):
    __tablename__ = 'family'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
    with_species = db.relationship('Species', backref='family')


class Genus(db.Model):
    __tablename__ = 'genus'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
    with_species = db.relationship('Species', backref='genus')


class Species(db.Model):
    __tablename__ = 'species'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
    genus_id = db.Column(db.Integer, db.ForeignKey('genus.id'))
    family_id = db.Column(db.Integer, db.ForeignKey('family.id'))
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    class_id = db.Column(db.Integer, db.ForeignKey('class.id'))
    divisionOrPhylum_id = db.Column(db.Integer, db.ForeignKey('divisionOrPhylum.id'))
    kingdom_id = db.Column(db.Integer, db.ForeignKey('kingdom.id'))


@app.route('/')
def func():
    return render_template('index.html')


KINGDOMS = {1: 'флора', 2: 'фауна'}


class SpeciesForm(FlaskForm):
    find = StringField(validators=[Optional(strip_whitespace=True)], default='')
    kingdom = RadioField('Выберите растения или животных', coerce=int, choices=KINGDOMS.items())
    button = SubmitField('фильтр')


class SearchForm(FlaskForm):
    kingdom = StringField(validators=[Optional(strip_whitespace=True)])
    find = StringField('название', validators=[DataRequired(message='Обязательное поле')], default='')
    findButton = SubmitField('найти')


@app.route('/species', methods=['GET', 'POST'])
def species():
    form1 = SpeciesForm()
    form2 = SearchForm()
    if form2.validate_on_submit():
        search = Species.query.filter(Species.name.like(f'%{form2.find.data}%')).all()
        species_result = Species.query.filter_by(kingdom_id=form1.kingdom.data).all()
        return render_template('species.html', search=search, species_result=species_result, form1=form1, form2=form2)
    if form1.validate_on_submit():
        species_result = Species.query.filter_by(kingdom_id=form1.kingdom.data).all()
        return render_template('species.html', species_result=species_result, form1=form1, form2=form2)
    return render_template('species.html', form1=form1, form2=form2)


if __name__ == '__main__':
    app.run(debug=True)
