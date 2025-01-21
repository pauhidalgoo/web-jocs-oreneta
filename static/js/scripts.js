// Function to dynamically update the leaderboard (using AJAX)
function updateLeaderboard() {
    fetch('/leaderboard') // Make a request to the leaderboard route
      .then(response => response.text())
      .then(html => {
        // Parse the HTML response
        const parser = new DOMParser();
        const doc = parser.parseFromString(html, 'text/html');
  
        // Get the updated leaderboard table
        const newLeaderboard = doc.querySelector('.leaderboard-container table');
  
        // Replace the old leaderboard with the updated one
        const oldLeaderboard = document.querySelector('.leaderboard-container table');
        if (oldLeaderboard && newLeaderboard) {
          oldLeaderboard.parentNode.replaceChild(newLeaderboard, oldLeaderboard);
        }
      })
      .catch(error => {
        console.error('Error updating leaderboard:', error);
      });
  }
  
  // Function to reveal a game (called by admin action)
  function revealGame(gameId) {
    const gameElement = document.getElementById(`game-${gameId}`);
    if (gameElement) {
      gameElement.classList.remove('game-hidden');
      gameElement.classList.add('game-revealed');
  
      // Remove the "Reveal" button
      const revealButton = gameElement.querySelector('.reveal-button');
      if (revealButton) {
        revealButton.remove();
      }
      
      // Add additional elements if needed (e.g., forms for team registration)
      if (gameElement.querySelector('.game-revealed-content')) {
          gameElement.querySelector('.game-revealed-content').style.display = 'block';
      }
    }
  }
  
  // Function to complete a game (called by admin action)
  function completeGame(gameId) {
    const gameElement = document.getElementById(`game-${gameId}`);
    if (gameElement) {
      gameElement.classList.remove('game-revealed');
      gameElement.classList.add('game-completed');
      
      // Remove the "Complete" button
      const completeButton = gameElement.querySelector('.complete-button');
      if (completeButton) {
        completeButton.remove();
      }
    }
  }
  
  // Call updateLeaderboard initially
  updateLeaderboard();
  
  // Set interval to update the leaderboard periodically (e.g., every 5 seconds)
  setInterval(updateLeaderboard, 5000);
  
  // Function to handle team registration submission
  function handleTeamRegistration(form) {
      const formData = new FormData(form);
      fetch(form.action, {
          method: 'POST',
          body: formData
      })
      .then(response => {
          if (!response.ok) {
              return response.text().then(text => { throw new Error(text) });
          }
          return response.text();
      })
      .then(data => {
          alert('Team registered successfully!');
          // Optionally, update the game timeline or other relevant elements
      })
      .catch(error => {
          alert('Error registering team: ' + error.message);
      });
  }
  
  // Event listener for team registration forms
  document.addEventListener('DOMContentLoaded', () => {
      const teamRegistrationForms = document.querySelectorAll('.timeline form');
      teamRegistrationForms.forEach(form => {
          form.addEventListener('submit', (event) => {
              event.preventDefault();
              handleTeamRegistration(form);
          });
      });
  });
  
  // Function to handle joining a team
  function handleJoinTeam(form) {
      const formData = new FormData(form);
      fetch(form.action, {
          method: 'POST',
          body: formData
      })
      .then(response => {
          if (!response.ok) {
              return response.text().then(text => { throw new Error(text) });
          }
          return response.text();
      })
      .then(data => {
          alert('Successfully joined the team!');
          // Optionally, update the game timeline or other relevant elements
      })
      .catch(error => {
          alert('Error joining team: ' + error.message);
      });
  }
  
  // Event listener for join team forms
  document.addEventListener('DOMContentLoaded', () => {
      const joinTeamForms = document.querySelectorAll('.timeline form[action^="/join_team/"]');
      joinTeamForms.forEach(form => {
          form.addEventListener('submit', (event) => {
              event.preventDefault();
              handleJoinTeam(form);
          });
      });
  });
  function filterEliminatoryLeaderboard() {
    const selectedGameId = document.getElementById("game-select").value;
    const playerBoxes = document.querySelectorAll(".eliminatory-leaderboard-grid .player-box");

    playerBoxes.forEach(box => {
        const gameIds = box.dataset.gameId.split(",").map(id => id.trim());

        if (selectedGameId === "" || gameIds.includes(selectedGameId)) {
            box.style.display = "block";
        } else {
            box.style.display = "none";
        }
    });
}
  
  // Function to handle voting in the final game
  function handleVote(form) {
      const formData = new FormData(form);
      fetch(form.action, {
          method: 'POST',
          body: formData
      })
      .then(response => {
          if (!response.ok) {
              return response.text().then(text => { throw new Error(text) });
          }
          return response.text();
      })
      .then(data => {
          alert('Vote submitted successfully!');
          // Optionally, update the leaderboard or other relevant elements
      })
      .catch(error => {
          alert('Error submitting vote: ' + error.message);
      });
  }
  
  // Event listener for vote forms
  document.addEventListener('DOMContentLoaded', () => {
      const voteForms = document.querySelectorAll('.timeline form[action^="/vote/"]');
      voteForms.forEach(form => {
          form.addEventListener('submit', (event) => {
              event.preventDefault();
              handleVote(form);
          });
      });
  });