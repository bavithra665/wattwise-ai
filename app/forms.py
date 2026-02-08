from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, FileField
from wtforms.validators import DataRequired, Length
from werkzeug.utils import secure_filename

class SettingsForm(FlaskForm):
    gemini_api_key = StringField('Gemini API Key', validators=[Length(min=1, max=255)])
    submit = SubmitField('Save Settings')

class UploadForm(FlaskForm):
    file = FileField('Energy Data File', validators=[DataRequired()])
    submit = SubmitField('Upload and Analyze')
