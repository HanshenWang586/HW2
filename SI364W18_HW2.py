## SI 364
## Winter 2018
## HW 2 - Part 1
# Hanshen Wang
# 40602121
# Jan 28

## This homework has 3 parts, all of which should be completed inside this file (and a little bit inside the /templates directory).

## Add view functions and any other necessary code to this Flask application code below so that the routes described in the README exist and render the templates they are supposed to (all templates provided are inside the templates/ directory, where they should stay).

## As part of the homework, you may also need to add templates (new .html files) to the templates directory.

#############################
##### IMPORT STATEMENTS #####
#############################
from flask import Flask, request, render_template, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, ValidationError
from wtforms.validators import Required, Length
import requests
import json

#####################
##### APP SETUP #####
#####################

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hardtoguessstring'
app.debug=True

####################
###### FORMS #######
####################

class AlbumEntryForm(FlaskForm):
    album = StringField('Enter the name of an album', validators=[Required()])
    number = RadioField('How much do you like this album?(1 low, 3 high)', choices=[(1,'1'),(2,'2'),(3,'3')], validators=[Required(),Length(1,3)])
    submit = SubmitField('Submit')
# Flaskform with album and number field


####################
###### ROUTES ######
####################

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/user/<name>')
def hello_user(name):
    return '<h1>Hello {0}<h1>'.format(name)

@app.route('/artistform')
def viewArtist():
	return render_template('artistform.html')
# render the template directly

@app.route('/artistinfo', methods = ['GET', 'POST'])
def infoResult():
	if request.method == 'GET':
		artist = request.args.get('artist')
		# get data from form
		response = requests.get('https://itunes.apple.com/search?term=' + artist + '&entity=musicTrack')
		# Request search result from iTunes API
		resultDic0 = json.loads(response.text)
		resultDic1 = resultDic0['results']
		# create a new dictionary under the json file, so that the new dicionary will contain only information about the track
		return render_template('artist_info.html',objects=resultDic1)
	return redirect(url_for('viewArtist'))
	# redirect user to the form page

@app.route('/artistlinks')
def viewLinks():
	return render_template('artist_links.html')

@app.route('/specific/song/<artist_name>')
def specificResult(artist_name):
    resp = requests.get('https://itunes.apple.com/search?term=' + artist_name + '&entity=musicTrack')
    data_text = resp.text 
    results0 = json.loads(data_text)
    results = results0['results']
    return render_template('specific_artist.html',results=results)

@app.route('/album_entry')
def entryView():
	simpleForm = AlbumEntryForm()
	return render_template('album_entry.html',form=simpleForm)

@app.route('/album_result',methods = ['GET', 'POST'])
def albumData():
	form = AlbumEntryForm()
	if request.method == 'POST':
		album = form.album.data
		number = form.number.data		
		resp = requests.get('https://itunes.apple.com/search?term=' + album + '&entity=album')
		# Request search result from iTunes API
		data_text = resp.text 
		results0 = json.loads(data_text)
		resultDic1 = results0['results']
		return render_template('album_data.html',objects=resultDic1,number=number)
	return redirect(url_for('entryView'))

if __name__ == '__main__':
    app.run(use_reloader=True,debug=True)
