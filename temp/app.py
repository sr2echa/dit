from flask import Flask, render_template

app = Flask(__name__)

json_data1 = {
    "__meta__" : [
        "7f61112bcecd967d4fbed3e05645c5a708eea1eb", "visualize database"
    ],

    "Shopers": [
        ["Name", "age", "ID","phone no."],
        ["harish", "19", "001","982834324"],
        ["nidish", "20", "002","234324232"],
        ["nidish", "20", "002","234324232"],
        ["nidish", "20", "002","234324232"],
        ["nidish", "20", "002","234324232"],
        ["nidish", "20", "002","234324232"],
        ["nidish", "20", "002","234324232"],
        ["nidish", "20", "002","234324232"],
        ["nidish", "20", "002","234324232"],
        ["nidish", "20", "002","234324232"],
        ["nidish", "20", "002","234324232"],
        ["nidish", "20", "002","234324232"],
        ["nidish", "20", "002","234324232"],
        ["nidish", "20", "002","234324232"],
        ["nidish", "20", "002","234324232"],
        ["nidish", "20", "002","234324232"],
        ["nidish", "20", "002","234324232"],
        ["nidish", "20", "002","234324232"],
        ["nidish", "20", "002","234324232"]
    ],
    "Flight DB: ": [
        ["Name", "age", "ID","phone no."],
        ["harish", "19", "001","982834324"],
        ["nidish", "20", "002","234324232"],
        ["nidish", "20", "002","234324232"],
        ["nidish", "20", "002","234324232"],
        ["nidish", "20", "002","234324232"],
        ["nidish", "20", "002","234324232"],
        ["nidish", "20", "002","234324232"],
        ["nidish", "20", "002","234324232"],
        ["nidish", "20", "002","234324232"],
        ["nidish", "20", "002","234324232"],
        ["nidish", "20", "002","234324232"],
        ["nidish", "20", "002","234324232"],
        ["nidish", "20", "002","234324232"],
        ["nidish", "20", "002","234324232"],
        ["nidish", "20", "002","234324232"],
        ["nidish", "20", "002","234324232"],
        ["nidish", "20", "002","234324232"],
        ["nidish", "20", "002","234324232"],
        ["nidish", "20", "002","234324232"]
    ],
    "blacklisted": [
        ["Name", "age", "ID","phone no."],
        ["harish", "19", "001","982834324"],
        ["nidish", "20", "002","234324232"],
        ["nidish", "20", "002","234324232"],
        ["nidish", "20", "002","234324232"],
        ["nidish", "20", "002","234324232"],
        ["nidish", "20", "002","234324232"],
        ["nidish", "20", "002","234324232"],
        ["nidish", "20", "002","234324232"],
        ["nidish", "20", "002","234324232"],
        ["nidish", "20", "002","234324232"],
        ["nidish", "20", "002","234324232"],
        ["nidish", "20", "002","234324232"],
        ["nidish", "20", "002","234324232"],
        ["nidish", "20", "002","234324232"],
        ["nidish", "20", "002","234324232"],
        ["nidish", "20", "002","234324232"],
        ["nidish", "20", "002","234324232"],
        ["nidish", "20", "002","234324232"],
        ["nidish", "20", "002","234324232"]
    ],
    "Temp": [
        ["Name", "age", "ID","phone no.","Name", "age", "ID","phone no.","phone no.","Name", "age", "ID","phone no."],
        ["harish", "19", "001","982834324"],
        ["nidish", "20", "002","234324232"],
        ["nidish", "20", "002","234324232"],
        ["nidish", "20", "002","234324232"],
        ["nidish", "20", "002","234324232"],
        ["nidish", "20", "002","234324232"],
        ["nidish", "20", "002","234324232"],
        ["nidish", "20", "002","234324232"],
        ["nidish", "20", "002","234324232"],
        ["nidish", "20", "002","234324232"],
        ["nidish", "20", "002","234324232"],
        ["nidish", "20", "002","234324232"],
        ["nidish", "20", "002","234324232"],
        ["nidish", "20", "002","234324232"],
        ["nidish", "20", "002","234324232"],
        ["nidish", "20", "002","234324232"],
        ["nidish", "20", "002","234324232"],
        ["nidish", "20", "002","234324232"],
        ["nidish", "20", "002","234324232"]
    ],
    "table8": [
        ["Name", "age", "ID","phone no."],
        ["harish", "19", "001","982834324"],
        ["nidish", "20", "002","234324232"],
        ["nidish", "20", "002","234324232"],
        ["nidish", "20", "002","234324232"],
        ["nidish", "20", "002","234324232"],
        ["nidish", "20", "002","234324232"],
        ["nidish", "20", "002","234324232"],
        ["nidish", "20", "002","234324232"],
        ["nidish", "20", "002","234324232"],
        ["nidish", "20", "002","234324232"],
        ["nidish", "20", "002","234324232"],
        ["nidish", "20", "002","234324232"],
        ["nidish", "20", "002","234324232"],
        ["nidish", "20", "002","234324232"],
        ["nidish", "20", "002","234324232"],
        ["nidish", "20", "002","234324232"],
        ["nidish", "20", "002","234324232"],
        ["nidish", "20", "002","234324232"],
        ["nidish", "20", "002","234324232"]
    ],
    "table9": [
        ["Name", "age", "ID","phone no."],
        ["harish", "19", "001","982834324"],
        ["nidish", "20", "002","234324232"],
        ["nidish", "20", "002","234324232"],
        ["nidish", "20", "002","234324232"],
        ["nidish", "20", "002","234324232"],
        ["nidish", "20", "002","234324232"],
        ["nidish", "20", "002","234324232"],
        ["nidish", "20", "002","234324232"],
        ["nidish", "20", "002","234324232"],
        ["nidish", "20", "002","234324232"],
        ["nidish", "20", "002","234324232"],
        ["nidish", "20", "002","234324232"],
        ["nidish", "20", "002","234324232"],
        ["nidish", "20", "002","234324232"],
        ["nidish", "20", "002","234324232"],
        ["nidish", "20", "002","234324232"],
        ["nidish", "20", "002","234324232"],
        ["nidish", "20", "002","234324232"],
        ["nidish", "20", "002","234324232"]
    ],
    "table0": [
        ["Name", "age", "ID","phone no."],
        ["harish", "19", "001","982834324"],
        ["nidish", "20", "002","234324232"],
        ["nidish", "20", "002","234324232"],
        ["nidish", "20", "002","234324232"],
        ["nidish", "20", "002","234324232"],
        ["nidish", "20", "002","234324232"],
        ["nidish", "20", "002","234324232"],
        ["nidish", "20", "002","234324232"],
        ["nidish", "20", "002","234324232"],
        ["nidish", "20", "002","234324232"],
        ["nidish", "20", "002","234324232"],
        ["nidish", "20", "002","234324232"],
        ["nidish", "20", "002","234324232"],
        ["nidish", "20", "002","234324232"],
        ["nidish", "20", "002","234324232"],
        ["nidish", "20", "002","234324232"],
        ["nidish", "20", "002","234324232"],
        ["nidish", "20", "002","234324232"],
        ["nidish", "20", "002","234324232"]
    ]
}


@app.route('/visualize')
def visualize():
    # Render the HTML template and pass JSON data to its
    meta_data = json_data1.get("__meta__", [])

    data_without_meta = {key: value for key, value in json_data1.items() if key != "__meta__"}

    return render_template('template_vis.html', data=data_without_meta, meta_data= meta_data)

if __name__ == '__main__':
    app.run(debug=True)

  
