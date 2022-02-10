from flask import Flask, render_template, request
from forms import ShiftForm, ConversionForm
app = Flask(__name__)
app.config["SECRET_KEY"] = "this-is-my-secret-key" # this line is also for security purposes

@app.route('/shift', methods=["GET","POST"])
def shift():
    
    form = ShiftForm()
    plaintext = form.plaintext.data
    shift = form.shift.data

    ciphertext=""
    if form.validate_on_submit():
        for char in plaintext:
            if char.isupper():
                ciphertext += chr((ord(char) - 65 + shift) % 26 + 65)
            elif char.islower():
                ciphertext += chr((ord(char) - 97 + shift) % 26 + 97)
            else:
                ciphertext += char
    
        form.ciphertext.data = ciphertext
    return render_template('shift.html', form=form, title="Caesar's Cipher")

@app.route('/conversion', methods=["GET","POST"])
def conversion():
    form = ConversionForm()
    

    if form.validate_on_submit():
        input_scale = form.input_scale.data
        input = form.input.data
        output_scale = form.output_scale
        output = None

        if input_scale == 'Kelvin:':
            if output_scale == 'Celsius:':
                output = input-273
            elif output_scale == 'Kelvin:':
                output=input
            else:
                output = 9/5 * (input-273) +32

        elif input_scale == 'Celsius:':
            if output_scale == 'Celsius:':
                output=input
            elif output_scale == 'Kelvin:':
                output = input+273
            else:
                output = 9/5 * input + 32

        else:
            if output_scale == 'Celsius:':
                output = 5/9 * (input-32)
            elif output_scale == 'Fahrenheit:':
                output = input
            else:
                output = 5/9 * (input-32) + 273
        
        form.output.data = output
    return render_template('conversion.html', form=form, title='Temperature Conversion')