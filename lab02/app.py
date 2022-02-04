from flask import Flask, render_template, request
import urllib.request, json

app = Flask(__name__)

@app.route('/spy', methods=['GET','POST'])
def spy():
    if request.method == 'GET':
        return render_template('spy_form.html')
    
    else:
        given_name = request.form['given_name']
        family_name = request.form['family_name']

        return render_template('spy_response.html', given_name=given_name, family_name=family_name)



@app.route('/morse', methods=['GET','POST'])
def morse():
    if request.method == "GET":
        return render_template("morse_form.html")
    else:
        try:
            message = request.form["message"]

            if message == "": 
                error = 'No message entered.'
                return render_template('morse_form.html', error = error)
            
            morse = ""


            cleaned_message = message.strip().upper()

            morse_dict = {
                        'A':'.-', 'B':'-...',
                        'C':'-.-.', 'D':'-..', 'E':'.',
                        'F':'..-.', 'G':'--.', 'H':'....',
                        'I':'..', 'J':'.---', 'K':'-.-',
                        'L':'.-..', 'M':'--', 'N':'-.',
                        'O':'---', 'P':'.--.', 'Q':'--.-',
                        'R':'.-.', 'S':'...', 'T':'-',
                        'U':'..-', 'V':'...-', 'W':'.--',
                        'X':'-..-', 'Y':'-.--', 'Z':'--..',
                        '1':'.----', '2':'..---', '3':'...--',
                        '4':'....-', '5':'.....', '6':'-....',
                        '7':'--...', '8':'---..', '9':'----.',
                        '0':'-----', ', ':'--..--', '.':'.-.-.-',
                        '?':'..--..', '/':'-..-.', '-':'-....-',
                        '(':'-.--.', ')':'-.--.-', ' ':'/'
                        }
            
            for char in cleaned_message:
                morse += morse_dict[char]
            
            return render_template('morse_response.html', morse=morse, message=message)
        except KeyError:
            error = 'Invalid character entered.'
            return render_template('morse_form.html', error=error)

@app.route('/lengths', methods=['GET','POST'])
def lengths():
    if request.method == 'GET':
        return render_template('lengths_form.html',inches="",centimetres="")
    else:
        inches = request.form['inches']
        centimetres = request.form['centimetres']

        # Check if both forms are filled, if so return the form with an error
        if (inches != '') and (centimetres != ''):
            error = 'Both fields are filled.'
            return render_template('lengths_form.html', error = error)

        elif (inches == '') and (centimetres == ''):
            error = 'Both fields are empty.'
            return render_template('lengths_form.html', error = error)
        
        else: 
            if inches == '':
                inches = round(float(centimetres)/2.54,2)
            else:
                centimetres = round(float(inches)*2.54,2)
            
            return render_template('lengths_form.html', inches=inches,centimetres=centimetres)
        
@app.route('/spy_name', methods=['GET','POST'])
def spy_name():
    if request.method == 'GET':
        return render_template('spy_name_form.html', error="",new_first_name="", new_second_name="")
    else:
        given_name = request.form['given_name']
        birthday = request.form['birthday']

        if (birthday =='') or (given_name ==''):
            error = 'Information missing.'
            return render_template('spy_name_form.html', error = error, new_first_name="", new_second_name="")
        
        spy_first_names =   [
                            'Golden','Red','Rogue','Alpha','Iron','Secret','Hot',
                            'Green','Hugh','Wild','Silver','Slick','Big','Deadly',
                            'Flash','Black','Cold','Wild','Dark','Blue','Stone',
                            'Lone','Sly','Sterling','Ultimate','Rocket'
                            ]
        
        spy_second_names =  [
                            'Danger','Spider','Lightning','Ghost','Ninja','Wolf',
                            'Storm','Scorpion','Cobra','Shadow','Jaguar','Jeegoh'
                            ]

        # Convert given_name to upper case, for ord calculation below
        given_name = given_name.upper()

        new_first_name = spy_first_names[( ord(given_name[0])-65 )]

        # The input type date ("birthday") always returns in the format - YYYY-MM-DD -> the month data is always stored at index 5 & 6.
        birth_month = int(birthday[5]+birthday[6])

        # birth_month -1 –> in order to change the month number to the corresponding index.
        new_second_name = spy_second_names[birth_month-1]

        return render_template('spy_name_form.html', error="", new_first_name = new_first_name, new_second_name = new_second_name)

@app.route('/xchange', methods=['GET','POST'])
def xchange():
    if request.method=="GET":
        return render_template('xchange.html', result="", user_input="")
    else:
        currency = request.form['currency']
        user_input = request.form['user_input']


        API_url = "http://api.exchangeratesapi.io/v1/latest?access_key=b8332a67e8775b84556eb418874799cf&base=EUR&symbols=CNY,GBP,JPY,USD"

        result = json.loads(urllib.request.urlopen(API_url).read())
        xchange_rates = result['rates']

        result = float(user_input) * xchange_rates[currency]
        CNY_checked = None
        GBP_checked = None
        JPY_checked = None
        USD_checked = None

        if currency=='CNY':
            CNY_checked = 'checked'
        elif currency=='GBP':
            GBP_checked = 'checked'
        elif currency=='JPY':
            JPY_checked = 'checked'
        else:
            USD_checked = 'checked'



        jinja_parameters = dict(result=result,user_input=user_input,CNY_checked=CNY_checked, GBP_checked=GBP_checked, JPY_checked=JPY_checked, USD_checked=USD_checked)

        return render_template('xchange.html', **jinja_parameters)