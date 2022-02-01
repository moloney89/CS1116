from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/morse", methods=["GET","POST"])
def morse():
    if request.method == "GET":
        return render_template("morse_form.html")
    else:
        message = request.form["message"]
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


@app.route('/bmi', methods=["GET","POST"])
def bmi():
    if request.method == "GET":
        return render_template("bmi_form.html", bmi="",height="",weight="")
    else:
        height = float(request.form["height"])
        weight = float(request.form["weight"])

        bmi = weight/(height**2)

        return render_template("bmi_form.html", bmi=bmi, height=height,weight=weight)