document.addEventListener('DOMContentLoaded', function() {
    showTab('addWorkout');
});

function showTab(tabId) {
    document.querySelectorAll('.tab-content').forEach(function(tab) {
        tab.style.display = 'none';
    });
    document.getElementById(tabId).style.display = 'block';

    if (tabId === 'addWorkout') {
        loadAddWorkoutContent();
    } else if (tabId === 'history') {
        loadHistoryContent();
    }
}

function loadAddWorkoutContent() {
    document.getElementById('addWorkout').innerHTML = `
        <h1>Add Workout</h1>
        <form id="workoutForm" class="needs-validation" novalidate>
            <div class="form-group">
                <label for="bench">Bench</label>
                <div class="exercise-row">
                    <input type="text" class="form-control square-input" name="bench_set1" required>
                    <input type="text" class="form-control square-input" name="bench_set2" required>
                    <input type="text" class="form-control square-input" name="bench_set3" required>
                </div>
            </div>
            <div class="form-group">
                <label for="squat">Squat</label>
                <div class="exercise-row">
                    <input type="text" class="form-control square-input" name="squat_set1" required>
                    <input type="text" class="form-control square-input" name="squat_set2" required>
                    <input type="text" class="form-control square-input" name="squat_set3" required>
                </div>
            </div>
            <button type="submit" class="btn btn-primary save-workout">Save Workout</button>
        </form>
    `;

    document.getElementById('workoutForm').addEventListener('submit', function(event) {
        event.preventDefault();
        if (this.checkValidity() === false) {
            event.stopPropagation();
        } else {
            const formData = new FormData(this);
            formData.append('timestamp', new Date().toISOString());
            fetch('/add_workout', {
                method: 'POST',
                body: formData
            }).then(response => response.json())
              .then(data => {
                  if (data.status === 'success') {
                      alert('Workout added successfully!');
                      loadHistoryContent(); // Update history after adding a workout
                      showTab('history');
                  }
              }).catch(error => {
                  console.error('Error:', error);
                  alert('An error occurred while adding the workout.');
              });
        }
        this.classList.add('was-validated');
    });
}

function loadHistoryContent() {
    fetch('/get_workouts')
        .then(response => response.json())
        .then(data => {
            let html = '<h1>Workout History</h1><table class="table"><thead><tr><th>Date</th><th>Time</th><th>Exercise</th><th>Set 1</th><th>Set 2</th><th>Set 3</th></tr></thead><tbody>';
            data.forEach(row => {
                const [date, time] = row.timestamp.split('T');
                const formattedTime = time.split('.')[0]; // Remove milliseconds
                html += `<tr><td>${date}</td><td>${formattedTime}</td><td>${row.exercise}</td><td>${row.set1}</td><td>${row.set2}</td><td>${row.set3}</td></tr>`;
            });
            html += '</tbody></table>';
            document.getElementById('history').innerHTML = html;
        });
}
