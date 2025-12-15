
let current = 0;
let times = Array(questions.length).fill(0);
let timers = Array(questions.length).fill(null);
let userAnswers = Array(questions.length).fill(null);
let results = Array(questions.length).fill(false);
let markedForReview = Array(questions.length).fill(false);

function updateStatusHeader() {
    let answered = userAnswers.filter(ans => ans !== null && ans !== '' && !(typeof ans === 'object' && Object.values(ans).every(v => v === ''))).length;
    let total = questions.length;
    let unattempted = total - answered;
    let toreview = markedForReview.filter(Boolean).length;
    document.getElementById('unattempted-count').textContent = unattempted;
    document.getElementById('answered-count').textContent = answered;
    document.getElementById('toreview-count').textContent = toreview;
    document.getElementById('total-count').textContent = total;
}

function startTimer(idx, qid) {
    if (timers[idx]) return;
    timers[idx] = setInterval(() => {
        times[idx]++;
        document.getElementById('timer-' + qid).textContent = `Time: ${times[idx]}s`;
    }, 1000);
}
function stopTimer(idx) {
    if (timers[idx]) { clearInterval(timers[idx]); timers[idx] = null; }
}
function showQuestion(idx) {
    document.querySelectorAll('.question-card').forEach((el, i) => {
        el.style.display = (i === idx) ? '' : 'none';
        // Highlight card if marked for review
        if (markedForReview[i]) {
            el.classList.add('border-warning');
        } else {
            el.classList.remove('border-warning');
        }
    });
    document.querySelectorAll('.nav-btn').forEach((btn, i) => {
        // Reset specific state classes but keep base class
        btn.classList.remove('active', 'marked', 'answered');

        // Apply classes based on state
        // 1. Mark for review (Highest priority visual)
        if (markedForReview[i]) {
            btn.classList.add('marked');
        }
        // 2. Answered
        else if (userAnswers[i] !== null && userAnswers[i] !== '' && !(typeof userAnswers[i] === 'object' && Object.values(userAnswers[i]).every(v => v === ''))) {
            btn.classList.add('answered');
        }

        // 3. Current Question Active State
        if (i === idx) {
            btn.classList.add('active');
        }
    });
    startTimer(idx, questions[idx].id);
    updateStatusHeader();
}
// Mark for Review button logic
document.querySelectorAll('.mark-btn').forEach((btn, idx) => {
    btn.addEventListener('click', function () {
        markedForReview[current] = !markedForReview[current];
        showQuestion(current);
    });
});
function getUserAnswer(idx) {
    const q = questions[idx];
    if (q.type === 'single') {
        const val = document.querySelector(`[name='answer-${q.id}']`).value;
        return val === '' ? null : val;
    } else if (q.type === 'dual') {
        const qVal = document.querySelector(`[name='answer-${q.id}-quotient']`).value;
        const rVal = document.querySelector(`[name='answer-${q.id}-remainder']`).value;
        return (qVal === '' && rVal === '') ? null : {
            quotient: qVal,
            remainder: rVal
        };
    } else if (q.type === 'text') {
        const val = document.querySelector(`[name='answer-${q.id}']`).value.trim();
        return val === '' ? null : val;
    }
    return null;
}
function checkAnswer(idx, userAns) {
    const q = questions[idx];
    let correct = false;
    if (q.type === 'single') {
        correct = Math.abs(Number(userAns) - Number(q.correct_answer)) < 0.01;
    } else if (q.type === 'dual') {
        correct = (Number(userAns.quotient) === q.correct_answer.quotient && Number(userAns.remainder) === q.correct_answer.remainder);
    } else if (q.type === 'text') {
        if (q.question_text.includes('prime factors')) {
            let ans = q.correct_answer.split(',').map(x => x.trim()).filter(x => x);
            let user = userAns.split(',').map(x => x.trim()).filter(x => x);
            correct = (ans.length === user.length && ans.every((v, i) => v == user[i]));
        } else if (q.question_text.includes('fraction')) {
            correct = (userAns.replace(/\s/g, '') === q.correct_answer.replace(/\s/g, ''));
        }
    }
    return correct;
}

function submitQuiz() {
    // Save current answer
    userAnswers[current] = getUserAnswer(current);
    // Evaluate all answers
    let score = 0;
    for (let i = 0; i < questions.length; i++) {
        results[i] = checkAnswer(i, userAnswers[i]);
        if (results[i]) score++;
    }
    document.getElementById('quiz-area').classList.add('hidden');
    document.getElementById('result-area').classList.remove('hidden');
    let totalTime = times.reduce((a, b) => a + b, 0);
    document.getElementById('score-summary').innerHTML = `Score: <b>${score} / ${questions.length}</b><br>Total Time: <b>${totalTime}s</b>`;
    // Fill result table
    let tbody = document.getElementById('result-table-body');
    tbody.innerHTML = '';
    for (let i = 0; i < questions.length; i++) {
        let q = questions[i];
        let userAns = userAnswers[i];
        let correctAns = q.correct_answer;
        let userAnsStr = '';
        let correctAnsStr = '';
        if (q.type === 'single') {
            userAnsStr = userAns;
            correctAnsStr = correctAns;
        } else if (q.type === 'dual') {
            userAnsStr = `Q: ${userAns.quotient}, R: ${userAns.remainder}`;
            correctAnsStr = `Q: ${correctAns.quotient}, R: ${correctAns.remainder}`;
        } else if (q.type === 'text') {
            userAnsStr = userAns;
            correctAnsStr = correctAns;
        }
        tbody.innerHTML += `<tr>
    <td>${i + 1}</td>
    <td>${q.question_text}</td>
    <td>${userAnsStr}</td>
    <td>${results[i] ? '<span class=\"text-success\">Correct</span>' : '<span class=\"text-danger\">Incorrect</span>'}</td>
    <td>${results[i] ? '' : correctAnsStr}</td>
    <td>${times[i]}</td>
</tr>`;
    }
}

document.querySelectorAll('.next-btn').forEach((btn, idx) => {
    btn.addEventListener('click', function () {
        stopTimer(current);
        userAnswers[current] = getUserAnswer(current);
        updateStatusHeader();
        if (current < questions.length - 1) {
            current++;
            showQuestion(current);
        }
    });
});
document.querySelectorAll('.prev-btn').forEach((btn, idx) => {
    btn.addEventListener('click', function () {
        stopTimer(current);
        userAnswers[current] = getUserAnswer(current);
        updateStatusHeader();
        if (current > 0) {
            current--;
            showQuestion(current);
        }
    });
});
document.querySelectorAll('.nav-btn').forEach((btn) => {
    btn.addEventListener('click', function () {
        stopTimer(current);
        userAnswers[current] = getUserAnswer(current);
        updateStatusHeader();
        const navIdx = parseInt(btn.getAttribute('data-nav'), 10);
        if (!isNaN(navIdx) && navIdx >= 0 && navIdx < questions.length) {
            current = navIdx;
            showQuestion(current);
        }
    });
});
document.querySelectorAll('.submit-btn').forEach((btn) => {
    btn.addEventListener('click', function () {
        stopTimer(current);
        userAnswers[current] = getUserAnswer(current);
        updateStatusHeader();
        submitQuiz();
    });
});
// Start first timer and update header
showQuestion(0);
updateStatusHeader();
