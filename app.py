from flask import Flask, render_template, request, redirect, url_for,send_from_directory,jsonify,session
from pymongo import MongoClient
import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

df = pd.read_csv('recommendation_dataset.csv')
df['Combined'] = df['Field of Study'] + " " + df['Course Description']

tfidf_vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf_vectorizer.fit_transform(df['Combined'].values.astype('U'))

def recommend_courses(field_of_study, num_recommendations=5):
    print(f"Field of Study Input: {field_of_study}")  
    user_tfidf = tfidf_vectorizer.transform([field_of_study])
    
   
    similarity_scores = cosine_similarity(user_tfidf, tfidf_matrix)
    
    print(f"Similarity Scores: {similarity_scores}") 
    
    sim_scores_df = pd.DataFrame(similarity_scores.flatten(), index=df.index, columns=['similarity'])
    sim_scores_df = sim_scores_df.sort_values(by='similarity', ascending=False).head(num_recommendations)
    
    print(f"Top Recommendations Indexes: {sim_scores_df.index}")  
    
    recommended_courses = df.loc[sim_scores_df.index]
    
    print(f"Recommended Courses: {recommended_courses}")  
    
    return recommended_courses.to_dict(orient='records')

@app.route('/recomm1')
def recomm1():
    return render_template('recomm1.html')


@app.route('/recommend', methods=['POST'])
def get_recommendations():
    field_of_study = request.form['field_of_study']
    recommendations = recommend_courses(field_of_study)
    return render_template('recommendations.html', recommendations=recommendations)

app.secret_key = os.urandom(24)
client = MongoClient('mongodb://localhost:27017/')
db = client['career']
users_collection = db['users']
collection = db['contacts']
careers_collection = db['careers']

@app.route('/')
def log():
    return render_template('login.html')

@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        majors = request.form['majors']
        skills = request.form['skills']
        salary = request.form['salary']
        colleges = request.form['colleges']

        career = {
            'title': title,
            'description': description,
            'majors': majors,
            'skills': skills,
            'salary': salary,
            'colleges': colleges
        }

        careers_collection.insert_one(career)
        return redirect(url_for('blog'))

    return render_template('form.html')


@app.route('/blog')
def blog():
    careers = careers_collection.find()
    return render_template('blog.html', careers=careers)


@app.route('/api/careers', methods=['GET'])
def get_careers():
    careers = list(careers_collection.find())
    for career in careers:
        career['_id'] = str(career['_id'])
    return jsonify(careers)


@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        if users_collection.find_one({'username': username}):
            return 'Username already exists!'
        else:
            users_collection.insert_one({'username': username, 'email':email,'password': password})
            session['username'] = username
            return redirect(url_for('profile'))
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users_collection.find_one({'username': username, 'password': password})
        if user:
            session['username'] = username
            return redirect(url_for('profile'))
        else:
            return 'Invalid username or password!'
    return render_template('login.html')    


@app.route('/profile')
def profile():
    if 'username' in session:
        username = session['username']
        user = users_collection.find_one({'username': username})
        if user:
            return render_template('profile.html', user=user)
    return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('log'))

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")

@app.route('/submit1', methods=['POST'])
def submit_contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        contact_data = {'name': name, 'email': email, 'message': message}
        collection.insert_one(contact_data)
        return redirect(url_for('home'))

@app.route('/thankyou')
def thank_you():
    return 'Thank you for contacting us!'

@app.route('/ai')
def ai():
    return render_template("ai.html")

@app.route('/counsellor')
def counsellor():
    return render_template("counsellor.html")

@app.route('/aviation')
def aviation():
    return render_template("aviation.html")

@app.route('/careerg')
def careerg():
    return render_template("careerg.html")

@app.route('/civil')
def civil():
    return render_template("civil.html")

@app.route('/civile')
def civile():
    return render_template("civile.html")

@app.route('/computer')
def computer():
    return render_template("computer.html")

@app.route('/electronics')
def electronics():
    return render_template("electronics.html")

@app.route('/electrical')
def electrical():
    return render_template("electrical.html")

@app.route('/mechanical')
def mechanical():
    return render_template("mechanical.html")

@app.route('/aeroscope')
def aeroscope():
    return render_template("aeroscope.html")

@app.route('/instrumental')
def instrumental():
    return render_template("instrumental.html")

@app.route('/design')
def design():
    return render_template("design.html")

@app.route('/education')
def education():
    return render_template("education.html")

@app.route('/enginee')
def enginee():
    return render_template("enginee.html")

@app.route('/finance')
def finance():
    return render_template("finance.html")

@app.route('/graduate')
def graduate():
    return render_template("graduate.html")

@app.route('/humani')
def humani():
    return render_template("humani.html")

@app.route('/manage')
def manage():
    return render_template("manage.html")

@app.route('/media')
def media():
    return render_template("media.html")

@app.route('/medici')
def medici():
    return render_template("medici.html")

@app.route('/sales')
def sales():
    return render_template("sales.html")

@app.route('/sur')
def sur():
    return render_template("sur.html")

@app.route('/ent')
def ent():
    return render_template("ent.html")

@app.route('/business')
def business():
    return render_template("business.html")

@app.route('/sports')
def sports():
    return render_template("sports.html")

@app.route('/project')
def project():
    return render_template("project.html")

@app.route('/event')
def event():
    return render_template("event.html")

@app.route('/fashion')
def fashion():
    return render_template("fashion.html")

@app.route('/doctor')
def doctor():
    return render_template("doctor.html")

@app.route('/pathology')
def pathology():
    return render_template("pathology.html")

@app.route('/veterinary')
def veterinary():
    return render_template("veterinary.html")

@app.route('/orthopadic')
def orthopadic():
    return render_template("orthopadic.html")

@app.route('/opthalmology')
def opthalmology():
    return render_template("opthalmology.html")

@app.route('/nursing')
def nursing():
    return render_template("nursing.html")

@app.route('/sucess')
def sucess():
    return render_template("sucess.html")


math_answers = ['a', 'b', 'a', 'a', 'c','b','a','d','a','b']
biology_answers = ['c', 'a', 'b', 'a', 'c','b','a','b','b','b']
arts_answers = ['c', 'c', 'c', 'c', 'c','b','a','a','c','c']
commerce_answers = ['d', 'a', 'c', 'a', 'c','d','c','c','b','c']


user_scores = {
    'math': 0,
    'biology': 0,
    'arts': 0,
    'commerce': 0
}


user_answers = {
    'math': [],
    'biology': [],
    'arts': [],
    'commerce': []
}

num_questions_per_subject = 10

@app.route('/aptitude')
def aptitude():
    all_tests_completed = all(len(user_answers[subject]) == num_questions_per_subject for subject in user_answers)
    return render_template('aptitude.html', all_tests_completed=all_tests_completed)

@app.route('/submit', methods=['POST'])
def submit():
    subject = request.form['subject']
    current_answers = [request.form.get(f'{subject}_question{i+1}') for i in range(num_questions_per_subject)]
    user_answers[subject] = current_answers
    
    if subject == 'math':
        user_scores['math'] = calculate_score(current_answers, math_answers)
    elif subject == 'biology':
        user_scores['biology'] = calculate_score(current_answers, biology_answers)
    elif subject == 'arts':
        user_scores['arts'] = calculate_score(current_answers, arts_answers)
    elif subject == 'commerce':
        user_scores['commerce'] = calculate_score(current_answers, commerce_answers)

    return redirect(url_for('aptitude'))


@app.route('/overall_result')
def overall_result():
    total_score = sum(user_scores.values())
    return render_template('result.html', user_scores=user_scores, total_score=total_score, total_questions=len(user_scores) * num_questions_per_subject)

def calculate_score(user_answers, answer_key):
    score = 0
    for i in range(len(user_answers)):
        if user_answers[i] == answer_key[i]:
            score += 1
    return score


@app.route('/career')
def career():
    max_score_subject = max(user_scores.items(), key=lambda x: x[1])
    return render_template('career.html', max_score_subject=max_score_subject)


if __name__ == '__main__':
    app.run(debug=True)
