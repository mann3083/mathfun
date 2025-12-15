// static/app.js

// --- 1. GLOBAL STATE ---
let current = 0;
let times = Array(questions.length).fill(0);
let timers = Array(questions.length).fill(null);
let userAnswers = Array(questions.length).fill(null);
let markedForReview = Array(questions.length).fill(false);
let results = Array(questions.length).fill(false);

// --- 2. CORE FUNCTIONS ---

function updateGlobalState() {
    // A. Update Counts
    let answeredCount = userAnswers.filter(a => isValidAnswer(a)).length;
    let reviewCount = markedForReview.filter(Boolean).length;

    document.getElementById('unattempted-count').textContent = questions.length - answeredCount;
    document.getElementById('answered-count').textContent = answeredCount;
    document.getElementById('toreview-count').textContent = reviewCount;
    document.getElementById('total-count').textContent = questions.length;

    // B. Update Sidebar Buttons
    document.querySelectorAll('.nav-btn').forEach(btn => {
        const idx = parseInt(btn.dataset.nav);

        // Reset classes safely
        btn.classList.remove('active', 'marked', 'answered');

        // Apply Color Priority
        if (markedForReview[idx]) {
            btn.classList.add('marked'); // Yellow
        } else if (isValidAnswer(userAnswers[idx])) {
            btn.classList.add('answered'); // Blue
        }

        // Apply Active Border
        if (idx === current) {
            btn.classList.add('active');
        }
    });

    // C. Show/Hide Question Cards
    document.querySelectorAll('.question-section').forEach((el, i) => {
        el.style.display = (i === current) ? 'block' : 'none';
    });
}

function isValidAnswer(ans) {
    if (ans === null) return false;
    if (typeof ans === 'object') {
        // For dual questions, valid if at least one field has text
        return ans.quotient !== '' || ans.remainder !== '';
    }
    return ans.toString().trim() !== '';
}

function getUserAnswer(idx) {
    const q = questions[idx];
    if (q.type === 'single' || q.type === 'text') {
        const el = document.querySelector(`[name='answer-${q.id}']`);
        // FIX: Trim whitespace so " " doesn't count as an answer
        return el.value.trim() === '' ? null : el.value.trim();
    } else if (q.type === 'dual') {
        const qVal = document.querySelector(`[name='answer-${q.id}-quotient']`).value.trim();
        const rVal = document.querySelector(`[name='answer-${q.id}-remainder']`).value.trim();
        return (qVal === '' && rVal === '') ? null : { quotient: qVal, remainder: rVal };
    }
}

// --- 3. NAVIGATION & EVENTS ---

function saveAndMove(newIdx) {
    stopTimer(current);
    userAnswers[current] = getUserAnswer(current);
    current = newIdx;
    startTimer(current);
    updateGlobalState();
}

// Sidebar Clicks
document.querySelectorAll('.nav-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        saveAndMove(parseInt(btn.dataset.nav));
    });
});

// Next/Prev Clicks
document.querySelectorAll('.next-btn').forEach(btn => btn.addEventListener('click', () => {
    if (current < questions.length - 1) saveAndMove(current + 1);
}));

document.querySelectorAll('.prev-btn').forEach(btn => btn.addEventListener('click', () => {
    if (current > 0) saveAndMove(current - 1);
}));

// Mark for Review
document.querySelectorAll('.mark-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        markedForReview[current] = !markedForReview[current];
        userAnswers[current] = getUserAnswer(current); // Sync answer state immediately
        updateGlobalState();
    });
});

// FIX: Prevent "Enter" key from reloading the page
document.addEventListener('keydown', function (event) {
    if (event.key === 'Enter') {
        event.preventDefault(); // Stop form submit
        // Optional: Make Enter click "Next"
        if (current < questions.length - 1) saveAndMove(current + 1);
    }
});

// Submit Button
document.querySelectorAll('.submit-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        stopTimer(current);
        userAnswers[current] = getUserAnswer(current);
        submitQuiz();
    });
});

// Real-time Input Validation for Navigation Colors
document.querySelectorAll('.answer-input').forEach(input => {
    input.addEventListener('input', () => {
        userAnswers[current] = getUserAnswer(current);
        updateGlobalState();
    });
});

// --- 4. TIMER LOGIC ---

function startTimer(idx) {
    if (timers[idx]) return;
    const qid = questions[idx].id;
    timers[idx] = setInterval(() => {
        times[idx]++;
        const el = document.getElementById(`timer-${qid}`);
        if (el) el.textContent = `Time: ${times[idx]}s`;
    }, 1000);
}

function stopTimer(idx) {
    if (timers[idx]) { clearInterval(timers[idx]); timers[idx] = null; }
}

// --- 5. GRADING LOGIC ---

function checkAnswer(idx, userAns) {
    const q = questions[idx];
    if (!isValidAnswer(userAns)) return false;

    if (q.type === 'single') {
        // Robust comparison for numbers (handles "5" vs 5)
        return Math.abs(Number(userAns) - Number(q.correct_answer)) < 0.01;
    } else if (q.type === 'dual') {
        return (Number(userAns.quotient) === q.correct_answer.quotient &&
            Number(userAns.remainder) === q.correct_answer.remainder);
    } else if (q.type === 'text') {
        if (q.question_text.includes('prime factors')) {
            // Sort to allow any order: "2, 3" == "3, 2"
            let ans = q.correct_answer.split(',').map(x => x.trim()).filter(x => x).sort((a, b) => a - b);
            let user = userAns.split(',').map(x => x.trim()).filter(x => x).sort((a, b) => a - b);
            return (ans.length === user.length && ans.every((v, i) => v == user[i]));
        } else if (q.question_text.includes('fraction')) {
            // Remove spaces: "1 / 2" -> "1/2"
            return (userAns.replace(/\s/g, '') === q.correct_answer.replace(/\s/g, ''));
        }
        return userAns.trim() === q.correct_answer;
    }
    return false;
}

function submitQuiz() {
    let score = 0;
    for (let i = 0; i < questions.length; i++) {
        results[i] = checkAnswer(i, userAnswers[i]);
        if (results[i]) score++;
    }

    // UI Cleanup for Result View
    document.getElementById('quiz-form').classList.add('d-none');
    document.getElementById('result-area').classList.remove('d-none');
    // Hide sidebar in results
    document.getElementById('sidebar-column').classList.add('d-none');
    document.getElementById('main-column').classList.replace('col-md-9', 'col-md-12');

    let totalTime = times.reduce((a, b) => a + b, 0);
    document.getElementById('score-summary').innerHTML =
        `Score: <b>${score} / ${questions.length}</b> &nbsp;|&nbsp; Total Time: <b>${totalTime}s</b>`;

    let tbody = document.getElementById('result-table-body');
    tbody.innerHTML = '';

    for (let i = 0; i < questions.length; i++) {
        let q = questions[i];
        let uAns = userAnswers[i];
        let cAns = q.correct_answer;

        // Format display
        let uStr = uAns;
        let cStr = cAns;

        if (q.type === 'dual') {
            uStr = uAns ? `Q: ${uAns.quotient}, R: ${uAns.remainder}` : 'No Answer';
            cStr = `Q: ${cAns.quotient}, R: ${cAns.remainder}`;
        } else if (uAns === null) {
            uStr = 'No Answer';
        }

        let status = results[i] ? 'Correct' : 'Incorrect';
        // Green row for correct, Red for incorrect
        let rowClass = results[i] ? 'table-success' : 'table-danger';

        tbody.innerHTML += `
            <tr class="${results[i] ? '' : 'table-light'}">
                <td>${i + 1}</td>
                <td>${q.question_text}</td>
                <td>${uStr}</td>
                <td class="${results[i] ? 'text-success' : 'text-danger'} fw-bold">${status}</td>
                <td>${cStr}</td>
                <td>${times[i]}</td>
            </tr>`;
    }
}

// --- 6. INITIALIZATION ---
updateGlobalState();
startTimer(0);