import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template
from groq import Groq  # Assuming the `groq` package is installed and available
 # Assuming you have a way to store/get the API key

app = Flask(__name__,static_folder='assets',template_folder='templates')

# Initialize Groq client with API key

app = Flask(__name__,static_folder='assets',template_folder='templates')

load_dotenv()

app = Flask(__name__,static_folder='assets',template_folder='templates')

# Fetch API key from environment variable
groq_api_key = os.getenv('GROQ_API_KEY')
if not groq_api_key:
    raise ValueError("API key not set in environment variables")

client = Groq(api_key=groq_api_key)

# Initial conversation context from .pages file

context = " u are the chatbot for reva university . and give the output as short as possible like in one statement in dialogue way . REVA University in Bengaluru is led by an esteemed panel of academic and industry experts, ensuring a blend of theoretical and practical learning. The Board of Management includes figures like Dr. P. Shyama Raju (Chancellor), Sri Umesh S. Raju (Pro-Chancellor), Dr. N. Ramesh (Vice-Chancellor in charge), and academic leaders such as Dr. Rajashekhar Biradar (Pro Vice Chancellor - Engineering) and Dr. Sanjay Chitnis (Pro Vice Chancellor - Strategic Initiatives). Advisory Board members include stalwarts like Prof. Bhimaraya Metri, Dr. M.D. Nalapat, and legal expert Ms. Divya Balagopal. Additionally, faculty across diverse departments bring years of academic, research, and industry experience, contributing to a robust curriculum. The university offers undergraduate and postgraduate programs across engineering, management, arts, science, law, and architecture, among others. Fee structures and seat availability vary by course, such as B.Tech programs starting at approximately ₹2.25 lakh per year. Specialized labs, workshops, and collaborations with industries provide students with hands-on experience, bridging the gap between academia and practical implementation. Placement records at REVA University are impressive, with top recruiters like TCS, Infosys, Wipro, and IBM visiting the campus regularly. Placement statistics reflect opportunities in diverse fields, with training programs and internships enhancing employability. Industry exposure is further amplified through guest lectures, workshops, and academic partnerships with global institutions. Located in Yelahanka, Bengaluru, the 45-acre green campus is equipped with state-of-the-art facilities, including libraries, sports complexes, hostels, and innovation hubs, fostering an enriching student life. REVA University offers a diverse range of courses with fee structures tailored to each program. The B.Tech programs, spanning specializations like Computer Science, Mechanical, and Civil Engineering, have fees ranging from ₹2.25 lakh to ₹4.50 lakh annually, depending on the branch and mode of entry (REVA CET, KCET, or other national-level exams). For M.Tech programs, which focus on areas like Data Science, Cybersecurity, and AI, the annual fees are between ₹1.50 lakh and ₹4.50 lakh. The B.Arch program, designed for aspiring architects, is priced at approximately ₹3 lakh per year. The MBA program, offering specializations in Marketing, Finance, HR, and Analytics, has a total fee of ₹6 lakh for the two-year course. Other undergraduate courses such as BBA and B.Com have an annual fee of ₹1.30 lakh to ₹1.45 lakh. For diploma and certification programs, fees begin at ₹25,000 per year, varying based on the duration and field of study. PhD programs across disciplines such as Engineering, Management, Science, and Arts are priced between ₹50,000 and ₹2.25 lakh annually.Law courses, including BA LLB and BBA LLB, are competitively priced at approximately ₹1.5–2 lakh annually. Specialized programs like M.Sc., MA, and MCA vary from ₹80,000 to ₹1.5 lakh annually based on the department and specialization. Scholarships and financial aid are available for meritorious and economically disadvantaged students, and specific fee reductions are offered based on entrance exam performance or other qualifying criteria.highest package is 54lpa in international companies.The annnual fest of reva is revostava .whuch is being celebrated superb grand at saugabdhika "
@app.route('/')
def index():
    return render_template('index1.html')

@app.route('/chat', methods=['POST'])
def chat():
    global context
    user_message = request.json.get("message")
    if not user_message:
        return jsonify({"error": "Empty message"}), 400

    # Prepare the messages for the Groq request
    messages = [
        {"role": "system", "content": context},
        {"role": "user", "content": user_message}
    ]

    # Create the completion request
    completion = client.chat.completions.create(
        model="llama-3.1-70b-versatile",
        messages=messages,
        temperature=1,
        max_tokens=1024,
        top_p=1,
        stream=True,
        stop=None,
    )

    # Collect the response from the streamed output
    response_content = ""
    for chunk in completion:
        response_content += chunk.choices[0].delta.content or ""

    # Append to the context for ongoing conversation
    context += f"\nUser: {user_message}\nAI: {response_content}"

    return jsonify({"message": response_content})

if __name__ == '__main__':
    print("I am the bot for REVA University.")
    app.run(debug=True)