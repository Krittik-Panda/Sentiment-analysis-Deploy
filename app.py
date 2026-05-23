from flask import Flask , render_template , url_for , redirect , request ,jsonify
import pickle
import os
from preprocess import clean_text, load_stopwords
from config import Config
from table import Prediction , db



app = Flask(__name__)
app.config.from_object(Config) #app.config is the Flask config object
db.init_app(app)



FEATURES_DIR = "features"
model      = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open(os.path.join(FEATURES_DIR, "vectorizer.pkl"), "rb"))
stopwords = load_stopwords("stop-words-list.txt")




@app.route("/", methods = ["GET"])
def welcome():
    return render_template("index.html")




@app.route('/history/')
def history_page():
    return render_template("history.html")




@app.route("/result/<string:label>")  
def result(label):
    return render_template("result.html" , label = label)  




@app.route("/predict/", methods = ["POST"])
def predict():
        input_text = str(request.form.get("tweet"))

        clean_input_text = clean_text(input_text, stopwords) # clean 
        X = vectorizer.transform([clean_input_text])
        if X.nnz == 0:
            labell = "Text contains no known vocabulary."
            return redirect(url_for('result' , label = labell))


        prediction = model.predict(X)
        probability = model.predict_proba(X)

        neg_prob = probability[0][0]
        pos_prob = probability[0][1]

     



        if 0.45 <= neg_prob <= 0.55 or 0.45 <= pos_prob <= 0.55:
            labell = "The text is neutral"
            
            #print(f"Probability is {probability}") 
        elif 0.50 <= neg_prob < 0.60:
            labell = "The text is neutral to negative"
            
            #print(f"Probability is {probability}")

        elif 0.50 <= pos_prob <= 0.60:
            labell = "The text is neutral to positive"
            
            #print(f"Probability is {probability}")

        else:
            labell = f"Text is {prediction[0]}"
            
            #print(f"Probability is {probability}")


        #add records to the database    

        data = Prediction(text= input_text,label = labell, pos_proba = float(probability[0][1]) , neg_proba = float(probability[0][0]))
        db.session.add(data)
        db.session.commit()
        return redirect(url_for('result' , label = labell))    


@app.route("/api/history", methods=["GET"])
def api_history_get():
    rows = Prediction.query.order_by(Prediction.created_at.desc()).all()

    history_data = []

    for r in rows:
        history_data.append({
            "id": r.id,
            "input_text": r.text,
            "result": r.label,
            "pos_prob": r.pos_proba,
            "neg_prob": r.neg_proba,
            "created_at": r.created_at.isoformat()
        })

    return jsonify({
        "data": history_data
    })


@app.route("/api/history", methods=["DELETE"])
def api_history_delete():
    Prediction.query.delete()
    db.session.commit()
    return jsonify({"message": "History cleared."})




if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug= True)
