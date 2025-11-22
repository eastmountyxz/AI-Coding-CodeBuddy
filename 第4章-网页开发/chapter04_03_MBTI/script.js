// MBTI Test Questions
const questions = [
    {
        question: "When attending a social event, you prefer to:",
        options: [
            { text: "Meet and talk to many different people (E)", value: "E" },
            { text: "Spend quality time with a few people you know (I)", value: "I" }
        ]
    },
    {
        question: "When making decisions, you tend to rely more on:",
        options: [
            { text: "Concrete facts and proven experiences (S)", value: "S" },
            { text: "Intuition and considering future possibilities (N)", value: "N" }
        ]
    },
    {
        question: "When evaluating a situation, you typically prioritize:",
        options: [
            { text: "Logical analysis and objective criteria (T)", value: "T" },
            { text: "Personal values and how people will be affected (F)", value: "F" }
        ]
    },
    {
        question: "In your daily life, you generally prefer:",
        options: [
            { text: "Having a structured schedule and clear plans (J)", value: "J" },
            { text: "Staying flexible and adapting as things come up (P)", value: "P" }
        ]
    },
    {
        question: "You find it more energizing to:",
        options: [
            { text: "Be in a lively, active environment with others (E)", value: "E" },
            { text: "Have quiet time alone to recharge (I)", value: "I" }
        ]
    },
    {
        question: "When learning something new, you prefer:",
        options: [
            { text: "Step-by-step instructions and practical applications (S)", value: "S" },
            { text: "Understanding the big picture and underlying concepts (N)", value: "N" }
        ]
    },
    {
        question: "When there's a conflict, you're more likely to consider:",
        options: [
            { text: "What is fair and reasonable based on principles (T)", value: "T" },
            { text: "How to maintain harmony and support everyone involved (F)", value: "F" }
        ]
    },
    {
        question: "When working on a project, you prefer to:",
        options: [
            { text: "Follow a clear plan with defined milestones (J)", value: "J" },
            { text: "Explore different approaches as you go along (P)", value: "P" }
        ]
    },
    {
        question: "You find it easier to:",
        options: [
            { text: "Start conversations and express your thoughts readily (E)", value: "E" },
            { text: "Listen carefully and think before speaking (I)", value: "I" }
        ]
    },
    {
        question: "You are more interested in:",
        options: [
            { text: "What is real and actual in the present moment (S)", value: "S" },
            { text: "What could be possible and imagining future scenarios (N)", value: "N" }
        ]
    },
    {
        question: "When giving feedback, you tend to be:",
        options: [
            { text: "Direct and straightforward about what needs improvement (T)", value: "T" },
            { text: "Tactful and encouraging, focusing on the positive (F)", value: "F" }
        ]
    },
    {
        question: "You prefer environments that are:",
        options: [
            { text: "Well-organized with clear expectations (J)", value: "J" },
            { text: "Relaxed and open to spontaneous changes (P)", value: "P" }
        ]
    },
    {
        question: "After a long week, you would rather:",
        options: [
            { text: "Go out with friends or to an event with others (E)", value: "E" },
            { text: "Spend time at home with a book or favorite show (I)", value: "I" }
        ]
    },
    {
        question: "You are more drawn to:",
        options: [
            { text: "Practical skills and useful knowledge (S)", value: "S" },
            { text: "Theoretical ideas and abstract concepts (N)", value: "N" }
        ]
    },
    {
        question: "When making a tough decision, you prioritize:",
        options: [
            { text: "Finding the most rational and efficient solution (T)", value: "T" },
            { text: "Considering how the decision affects everyone involved (F)", value: "F" }
        ]
    },
    {
        question: "Your workspace is typically:",
        options: [
            { text: "Organized with everything in its proper place (J)", value: "J" },
            { text: "Flexible with items arranged based on current projects (P)", value: "P" }
        ]
    },
    {
        question: "In group settings, you usually:",
        options: [
            { text: "Speak up and share your ideas readily (E)", value: "E" },
            { text: "Observe and listen before contributing (I)", value: "I" }
        ]
    },
    {
        question: "You are more likely to trust:",
        options: [
            { text: "Your direct experiences and what you can verify (S)", value: "S" },
            { text: "Your hunches and what feels right intuitively (N)", value: "N" }
        ]
    },
    {
        question: "When someone comes to you with a problem, you first:",
        options: [
            { text: "Analyze the situation and suggest solutions (T)", value: "T" },
            { text: "Listen empathetically and offer emotional support (F)", value: "F" }
        ]
    },
    {
        question: "You prefer to:",
        options: [
            { text: "Make decisions promptly and stick to them (J)", value: "J" },
            { text: "Keep options open and decide when necessary (P)", value: "P" }
        ]
    }
];

// MBTI Type Descriptions
const typeDescriptions = {
    "ISTJ": "Quiet, serious, and responsible. You're practical and fact-minded, with strong values. You tend to be thorough and dependable, valuing traditions and loyalty.",
    "ISFJ": "Quiet, friendly, and conscientious. You're committed to meeting obligations and serving others. You're practical, compassionate, and concerned with how your actions affect others.",
    "INFJ": "Idealistic and principled. You have deep insights about others and are committed to your values. You're organized and decisive in implementing your vision.",
    "INTJ": "Independent and analytical. You have high standards and original minds. You're driven to implement your ideas and achieve your goals with or without others' support.",
    "ISTP": "Tolerant and flexible. You're a keen observer of life who values efficiency. You're interested in cause and effect, organizing facts using logical principles, and excel at finding solutions to practical problems.",
    "ISFP": "Quiet, friendly, and sensitive. You enjoy the present moment and what's going on around you. You value personal space and working within your own time frame, loyal to values and people important to you.",
    "INFP": "Idealistic and loyal to your values. You seek to understand people and help them fulfill their potential. You're adaptable and flexible unless a value is threatened.",
    "INTP": "Logical and ingenious. You seek to develop logical explanations for everything that interests you. You're theoretical and abstract, more interested in ideas than social interaction.",
    "ESTP": "Flexible and tolerant. You take a pragmatic approach focused on immediate results. You're bored by theories, but enjoy solving problems with action. You live in the moment and enjoy material comforts.",
    "ESFP": "Outgoing, friendly, and accepting. You love life, people, and material comforts. You work well with others to make things happen. You bring common sense and a realistic approach to your work.",
    "ENFP": "Warmly enthusiastic and imaginative. You see life as full of possibilities. You make connections between events and information very quickly, proceeding confidently based on patterns you see.",
    "ENTP": "Quick, ingenious, and stimulating. You're adept at generating conceptual possibilities and then analyzing them strategically. You're good at reading others and bored by routine.",
    "ESTJ": "Practical, realistic, and decisive. You quickly move to implement decisions. You organize projects and people to get things done. You focus on results in the most efficient way possible.",
    "ESFJ": "Warmhearted, conscientious, and cooperative. You want harmony in your environment and work with determination to establish it. You value traditions and security.",
    "ENFJ": "Warm, empathetic, responsive, and responsible. You're highly attuned to others' emotions, needs, and motivations. You find potential in everyone and help others fulfill their potential.",
    "ENTJ": "Frank, decisive, and quick to take charge. You're good at logical reasoning and enjoy complex challenges. You see inefficiency and want to organize for efficiency."
};

// Variables to track test state
let currentQuestion = 0;
let answers = [];
let scores = {
    E: 0, I: 0,
    S: 0, N: 0,
    T: 0, F: 0,
    J: 0, P: 0
};

// DOM Elements
const introSection = document.getElementById('intro-section');
const questionSection = document.getElementById('question-section');
const resultsSection = document.getElementById('results-section');
const startBtn = document.getElementById('start-btn');
const questionText = document.getElementById('question-text');
const optionA = document.getElementById('option-a');
const optionB = document.getElementById('option-b');
const prevBtn = document.getElementById('prev-btn');
const nextBtn = document.getElementById('next-btn');
const progressBar = document.getElementById('progress');
const questionCounter = document.getElementById('question-counter');
const restartBtn = document.getElementById('restart-btn');
const mbtiTypeElement = document.getElementById('mbti-type');
const typeDescriptionElement = document.getElementById('type-description');

// Initialize the test
function initTest() {
    currentQuestion = 0;
    answers = Array(questions.length).fill(null);
    scores = {
        E: 0, I: 0,
        S: 0, N: 0,
        T: 0, F: 0,
        J: 0, P: 0
    };
    
    showSection(introSection);
}

// Show a specific section and hide others
function showSection(section) {
    introSection.classList.remove('active');
    questionSection.classList.remove('active');
    resultsSection.classList.remove('active');
    
    section.classList.add('active');
}

// Display the current question
function displayQuestion() {
    const question = questions[currentQuestion];
    questionText.textContent = question.question;
    optionA.textContent = question.options[0].text;
    optionB.textContent = question.options[1].text;
    
    // Update selected state
    optionA.classList.remove('selected');
    optionB.classList.remove('selected');
    
    if (answers[currentQuestion] === 0) {
        optionA.classList.add('selected');
    } else if (answers[currentQuestion] === 1) {
        optionB.classList.add('selected');
    }
    
    // Update progress
    const progress = ((currentQuestion + 1) / questions.length) * 100;
    progressBar.style.width = `${progress}%`;
    questionCounter.textContent = `Question ${currentQuestion + 1} of ${questions.length}`;
    
    // Update navigation buttons
    prevBtn.disabled = currentQuestion === 0;
    nextBtn.textContent = currentQuestion === questions.length - 1 ? 'See Results' : 'Next';
}

// Calculate MBTI type based on scores
function calculateMBTIType() {
    let type = '';
    type += scores.E > scores.I ? 'E' : 'I';
    type += scores.S > scores.N ? 'S' : 'N';
    type += scores.T > scores.F ? 'T' : 'F';
    type += scores.J > scores.P ? 'J' : 'P';
    return type;
}

// Display test results
function displayResults() {
    // Calculate final scores
    answers.forEach((answer, index) => {
        if (answer !== null) {
            const selectedOption = questions[index].options[answer];
            scores[selectedOption.value]++;
        }
    });
    
    // Calculate MBTI type
    const mbtiType = calculateMBTIType();
    
    // Display type and description
    mbtiTypeElement.textContent = mbtiType;
    typeDescriptionElement.textContent = typeDescriptions[mbtiType];
    
    // Update score bars
    updateScoreBar('e', 'i', scores.E, scores.I);
    updateScoreBar('s', 'n', scores.S, scores.N);
    updateScoreBar('t', 'f', scores.T, scores.F);
    updateScoreBar('j', 'p', scores.J, scores.P);
    
    showSection(resultsSection);
}

// Update score visualization bars
function updateScoreBar(type1, type2, score1, score2) {
    const total = score1 + score2;
    const percent1 = (score1 / total) * 100;
    const percent2 = (score2 / total) * 100;
    
    document.getElementById(`${type1}-bar`).style.width = `${percent1}%`;
    document.getElementById(`${type2}-bar`).style.width = `${percent2}%`;
    document.getElementById(`${type1}-score`).textContent = score1;
    document.getElementById(`${type2}-score`).textContent = score2;
}

// Event Listeners
startBtn.addEventListener('click', () => {
    showSection(questionSection);
    displayQuestion();
});

optionA.addEventListener('click', () => {
    answers[currentQuestion] = 0;
    optionA.classList.add('selected');
    optionB.classList.remove('selected');
    
    if (currentQuestion < questions.length - 1) {
        currentQuestion++;
        displayQuestion();
    }
});

optionB.addEventListener('click', () => {
    answers[currentQuestion] = 1;
    optionB.classList.add('selected');
    optionA.classList.remove('selected');
    
    if (currentQuestion < questions.length - 1) {
        currentQuestion++;
        displayQuestion();
    }
});

prevBtn.addEventListener('click', () => {
    if (currentQuestion > 0) {
        currentQuestion--;
        displayQuestion();
    }
});

nextBtn.addEventListener('click', () => {
    if (currentQuestion < questions.length - 1) {
        currentQuestion++;
        displayQuestion();
    } else {
        // Check if all questions are answered
        const unanswered = answers.findIndex(answer => answer === null);
        if (unanswered !== -1) {
            alert(`Please answer question ${unanswered + 1} before seeing results.`);
            currentQuestion = unanswered;
            displayQuestion();
        } else {
            displayResults();
        }
    }
});

restartBtn.addEventListener('click', () => {
    initTest();
});

// Initialize the test when the page loads
initTest();