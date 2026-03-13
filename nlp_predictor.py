from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

# Training dataset (sample)
problems = [
"chest pain",
"heart attack symptoms",
"severe breathing problem",
"high fever",
"vomiting and weakness",
"headache",
"stomach pain",
"cold and cough",
"minor injury",
"skin rash"
]

labels = [
"High",
"High",
"High",
"Medium",
"Medium",
"Low",
"Low",
"Low",
"Low",
"Low"
]

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(problems)

model = MultinomialNB()
model.fit(X, labels)

def predict_urgency(problem):

    x = vectorizer.transform([problem])
    urgency = model.predict(x)[0]

    return urgency