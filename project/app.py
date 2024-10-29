from flask import Flask, render_template, request, jsonify
from nltk.chat.util import Chat, reflections
import speech_recognition as sr
import pyttsx3
import threading

app = Flask(__name__)

patterns = [
    (r'hi|hello|hey', ['Hello!', 'Hi there!', 'Hey!']),
    (r'how are you|how are you doing', ['I am doing well, thank you!', 'I\'m fine, thanks!']),
    (r'how can i vote|how do i vote|how to vote|vote|how can we vote', ['To vote, log in to your account, navigate to the voting section, select the candidates or issues you want to vote on, and submit your ballot.',
                         'You can vote by logging into your account, going to the voting section, and selecting your preferred candidates or issues.']),
    (r'do i need to create an account to vote', ['Yes, creating an account is necessary to ensure the integrity of the voting process and to verify your eligibility to vote.',
                                                 'Absolutely, you need to create an account to vote. This helps us maintain a secure and fair voting system.']),
    (r'how do i create an account|how can i create an account', ['Click on the "Sign Up" button on the homepage, provide your email address, create a password, and follow the verification instructions sent to your email.',
                                     'To create an account, click "Sign Up" on the homepage, enter your email, create a password, and verify your email address.']),
    (r'how often can i vote', ['You can vote once per election or voting period for each ballot. Make sure to review your choices before submitting.',
                               'Voting is allowed once per election or voting period. Be sure to confirm your selections before finalizing your vote.']),
    (r'can i leave detailed feedback for a candidate', ['Yes, after voting, you can leave feedback on candidates and issues through the feedback section on our website.',
                                                        'Detailed feedback is encouraged and can be provided after you vote through our feedback form.']),
    (r'what should i do if i encounter a problem while voting', ['Use the "Report an Issue" feature available on the voting page to describe the problem. Our support team will assist you promptly.',
                                                                 'If you encounter a problem, report it using the "Report an Issue" feature on the voting page, and our support team will help.']),
    (r'how is my personal information protected', ['We use industry-standard security measures to protect your personal data. Please refer to our Privacy Policy for more details.',
                                                   'Your personal information is protected with industry-standard security measures. See our Privacy Policy for more details.']),
    (r'will my votes be anonymous', ['Yes, your votes are anonymous to ensure privacy and confidentiality. Only aggregated results are shared.',
                                     'Absolutely, your votes remain anonymous, and only aggregated results are made public.']),
    (r'can i suggest new candidates or issues to be added to the ballot', ['Yes, we welcome suggestions! Please use the "Suggest a Candidate/Issue" form on our website to submit your recommendations.',
                                                                          'You can suggest new candidates or issues via the "Suggest a Candidate/Issue" form on our website.']),
    (r'how are the election results determined', ['Election results are determined based on the total number of votes each candidate or issue receives, and results are verified for accuracy.',
                                                  'We determine election results by tallying the votes for each candidate or issue, with a thorough verification process for accuracy.']),
    (r'are there any rewards for participating in voting', ['Yes, active participants may receive rewards such as badges, recognition in our community, or entry into prize drawings. Check our "Rewards" page for current incentives.',
                                                            'Active voters can earn rewards like badges, community recognition, or prize draw entries. See our "Rewards" page for details.']),
    (r'who can i contact for further questions or issues', ['For any further questions or issues, you can contact our support team via the "Contact Us" page or email support@politicalvotingsite.com.',
                                                            'You can reach our support team through the "Contact Us" page or email us at support@politicalvotingsite.com.']),
    (r'what is your name?', ['You can call me Ghost.', 'I am just Ghost, your voting assistant.']),
    (r'bye|goodbye|thank you|thanks', ['Goodbye!', 'Bye Take care.']),
]

chatbot = Chat(patterns, reflections)

def spk_txt(word):
    engine = pyttsx3.init()
    engine.say(word)
    engine.runAndWait()

def recognize_speech():
    sp_eng = sr.Recognizer()
    with sr.Microphone() as mic:
        spk_txt("I'm listening")
        audio = sp_eng.listen(mic)
        try:
            mytxt = sp_eng.recognize_google(audio)
            return mytxt
        except sr.UnknownValueError:
            return "Sorry, I did not understand that."
        except sr.RequestError:
            return "Sorry, my speech service is down."

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    response = chatbot.respond(user_input)
    threading.Thread(target=spk_txt, args=(response,)).start()
    return jsonify({'response': response})

@app.route('/voice', methods=['POST'])
def voice():
    user_input = recognize_speech()
    response = chatbot.respond(user_input)
    threading.Thread(target=spk_txt, args=(response,)).start()
    return jsonify({'response': response, 'input': user_input})

if __name__ == '__main__':
    app.run(port = 5500,debug=True)
