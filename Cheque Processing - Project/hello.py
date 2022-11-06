from flask import Flask,request
from flask import render_template
from chequerecognizer import analyze_custom_documents
from chequerecognizer import model_id
from bankdatabase import cursor

app = Flask(__name__)

@app.route("/",methods=['GET'])
def hello_world():
    return render_template('index.html')

@app.route('/',methods=['POST'])
def predict():
    #getting cheque data thru OCR
    imagefile=request.files['imagefile']
    cheque_data=analyze_custom_documents(model_id,imagefile)
    print(cheque_data['Account No.'])
    query=f"SELECT * FROM client_data WHERE Account_Number={cheque_data['Account No.']};"
    cursor.execute(query)
    records = bool(cursor.fetchall())
    print(records)
    return render_template('index.html')


if __name__=='__main__':
    app.run(port=3000,debug=True)

