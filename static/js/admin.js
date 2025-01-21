// Function to update player score using AJAX
function updatePlayerScore(playerId, points) {
    const formData = new FormData();
    formData.append('player_id', playerId);
    formData.append('points', points);
  
    fetch('/admin/update_score', {
      method: 'POST',
      body: formData
    })
    .then(response => response.text())
    .then(result => {
      console.log(result); // Log the result (success or error message)
      // Update the score displayed on the page without reloading
      const scoreElement = document.querySelector(`#player-${playerId}-score`);
      if (scoreElement) {
        const currentScore = parseInt(scoreElement.textContent);
        scoreElement.textContent = currentScore + points;
      }
    })
    .catch(error => {
      console.error('Error updating score:', error);
    });
  }
  
  // Function to update team score using AJAX
  function updateTeamScore(teamId, points) {
    const formData = new FormData();
    formData.append('team_id', teamId);
    formData.append('points', points);
  
    fetch('/admin/update_team_score', {
      method: 'POST',
      body: formData
    })
    .then(response => response.text())
    .then(result => {
      console.log(result); // Log the result
      // Optionally, update the scores of team members displayed on the page
    })
    .catch(error => {
      console.error('Error updating team score:', error);
    });
  }
  
  // Function to eliminate a player using AJAX
  function eliminatePlayer(playerId, gameId) {
    if (!confirm('Are you sure you want to eliminate this player?')) {
      return;
    }
  
    const formData = new FormData();
    formData.append('player_id', playerId);
    formData.append('game_id', gameId);
  
    fetch('/admin/eliminate_player', {
      method: 'POST',
      body: formData
    })
    .then(response => response.text())
    .then(result => {
      console.log(result); // Log the result
  
      // Update the player row to indicate elimination (e.g., add a class)
      const playerRow = document.querySelector(`#player-row-${playerId}`);
      if (playerRow) {
        playerRow.classList.add('eliminatedadmin'); // Add a CSS class for styling
  
        // Optionally, disable the eliminate button for this player
        const eliminateButton = playerRow.querySelector('.eliminate-player-form button');
        if (eliminateButton) {
          eliminateButton.disabled = true;
          eliminateButton.textContent = 'Eliminated';
        }
      }
    })
    .catch(error => {
      console.error('Error eliminating player:', error);
    });
  }
  // Function to reveal a game using AJAX
  function revealGame(gameId) {
    fetch(`/admin/game/${gameId}/reveal`, {
      method: 'POST'
    })
    .then(response => response.text())
    .then(result => {
      console.log(result); // Log the result
      // Call the revealGame function in scripts.js to update the client-side
      window.opener.revealGame(gameId);
      
      // Update the button to "Mark as Complete"
      const button = document.querySelector(`#game-${gameId}-reveal`);
      if (button) {
        button.textContent = 'Mark as Complete';
        button.onclick = function() { completeGame(gameId); };
      }
    })
    .catch(error => {
      console.error('Error revealing game:', error);
    });
  }
  function startGame(gameId) {
    fetch(`/admin/game/${gameId}/start`, {
      method: 'POST'
    })
    .then(response => response.text())
    .then(result => {
      console.log(result); // Log the result
  
      // Update the button to "Mark as Complete"
      const button = document.querySelector(`#game-${gameId}-start`);
      if (button) {
        button.textContent = 'Mark as Complete';
        button.onclick = function() { completeGame(gameId); };
      }
    })
    .catch(error => {
      console.error('Error starting game:', error);
    });
  }
  
  // Function to complete a game using AJAX
  function completeGame(gameId) {
    fetch(`/admin/game/${gameId}/complete`, {
      method: 'POST'
    })
    .then(response => response.text())
    .then(result => {
      console.log(result); // Log the result
      // Call the completeGame function in scripts.js to update the client-side
      window.opener.completeGame(gameId);
      
      // Update the button to "Start Voting" if it is the final game
      const button = document.querySelector(`#game-${gameId}-complete`);
      if (button) {
          const gameNameElement = document.querySelector(`#game-${gameId}-name`);
          if (gameNameElement && gameNameElement.textContent.trim() === 'Final: Preguntes') {
              button.textContent = 'Start Voting';
              button.onclick = function() { startVoting(gameId); };
          } else {
              button.remove(); // Remove the button if not the final game
          }
      }
    })
    .catch(error => {
      console.error('Error completing game:', error);
    });
  }
  
  // Function to start voting for the final game using AJAX
  function startVoting(gameId) {
    fetch(`/admin/game/${gameId}/start_voting`, {
      method: 'POST'
    })
    .then(response => response.text())
    .then(result => {
      console.log(result);
      // Handle any necessary UI updates on the admin side
    })
    .catch(error => {
      console.error('Error starting voting:', error);
    });
  }

  function updatePlayerScore(playerId, points) {
    const formData = new FormData();
    formData.append('player_id', playerId);
    formData.append('points', points);
  
    fetch('/admin/update_score', {
      method: 'POST',
      body: formData
    })
    .then(response => response.text())
    .then(result => {
      console.log(result); // Log the result (success or error message)
      // Update the score displayed on the page without reloading
      const scoreElement = document.querySelector(`#player-${playerId}-score`);
      if (scoreElement) {
        const currentScore = parseInt(scoreElement.textContent);
        scoreElement.textContent = currentScore + points;
      }
    })
    .catch(error => {
      console.error('Error updating score:', error);
    });
  }
  
  // Function to update team score using AJAX
  function updateTeamScore(teamId, points) {
    const formData = new FormData();
    formData.append('team_id', teamId);
    formData.append('points', points);
  
    fetch('/admin/update_team_score', {
      method: 'POST',
      body: formData
    })
    .then(response => response.text())
    .then(result => {
      console.log(result); // Log the result
      // Optionally, update the scores of team members displayed on the page
    })
    .catch(error => {
      console.error('Error updating team score:', error);
    });
  }
  
  // Function to eliminate a player using AJAX
  function eliminatePlayer(playerId, gameId, action) {
    if (!confirm(`Are you sure you want to ${action} this player?`)) {
      return;
    }
  
    const formData = new FormData();
    formData.append('player_id', playerId);
    formData.append('game_id', gameId);
    formData.append('action', action); // Send 'eliminate' or 'uneliminate'
  
    fetch('/admin/eliminate_player', {
      method: 'POST',
      body: formData
    })
    .then(response => response.text())
    .then(result => {
      console.log(result);
  
      const playerRow = document.querySelector(`#player-row-${playerId}`);
      if (playerRow) {
        const eliminateButton = playerRow.querySelector('.eliminate-player-form button');
        const eliminateForm = playerRow.querySelector('.eliminate-player-form');
        if (eliminateButton) {
          if (action === 'eliminate') {
            playerRow.classList.add('eliminated');
            eliminateButton.textContent = 'Uneliminate';
            eliminateForm.querySelector('[name="action"]').value = 'uneliminate';
          } else {
            playerRow.classList.remove('eliminated');
            eliminateButton.textContent = 'Eliminate';
            eliminateForm.querySelector('[name="action"]').value = 'eliminate';
          }
        }
      }
    })
    .catch(error => {
      console.error('Error:', error);
    });
  }
  
  // Function to reveal a game using AJAX
  function revealGame(gameId) {
    fetch(`/admin/game/${gameId}/reveal`, {
      method: 'POST'
    })
    .then(response => response.text())
    .then(result => {
      console.log(result); // Log the result
      // Call the revealGame function in scripts.js to update the client-side
      window.opener.revealGame(gameId);
      
      // Update the button to "Mark as Complete"
      const button = document.querySelector(`#game-${gameId}-reveal`);
      if (button) {
        button.textContent = 'Mark as Complete';
        button.dataset.action = 'complete';
      }
    })
    .catch(error => {
      console.error('Error revealing game:', error);
    });
  }
  
  // Function to complete a game using AJAX
  function completeGame(gameId) {
    fetch(`/admin/game/${gameId}/complete`, {
      method: 'POST'
    })
    .then(response => response.text())
    .then(result => {
      console.log(result); // Log the result
      // Call the completeGame function in scripts.js to update the client-side
      window.opener.completeGame(gameId);
      
      // Update the button to "Start Voting" if it is the final game
      const button = document.querySelector(`#game-${gameId}-complete`);
      if (button) {
          const gameNameElement = document.querySelector(`#game-${gameId}-name`);
          if (gameNameElement && gameNameElement.textContent.trim() === 'Final: Preguntes') {
              button.textContent = 'Start Voting';
              button.dataset.action = 'start_voting';
          } else {
              button.remove(); // Remove the button if not the final game
          }
      }
    })
    .catch(error => {
      console.error('Error completing game:', error);
    });
  }

  function deleteGame(gameId) {
  
    fetch(`/admin/delete_game/${gameId}`, {
      method: 'POST'
    })
    .then(response => response.text())
    .then(result => {
      console.log(result); // Log the result
  
      // Remove the game row from the table
      const gameRow = document.querySelector(`#game-row-${gameId}`);
      if (gameRow) {
        gameRow.remove();
      }
    })
    .catch(error => {
      console.error('Error deleting game:', error);
    });
  }

  function searchPlayers() {
    var input, filter, table, tr, td, i, txtValue;
    input = document.getElementById("player-search");
    filter = input.value.toUpperCase();
    table = document.getElementById("players-table");
    tr = table.getElementsByTagName("tr");
    for (i = 0; i < tr.length; i++) {
      td = tr[i].getElementsByTagName("td")[0]; // Filter by first column (Player Number)
      if (td) {
        txtValue = td.textContent || td.innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
          tr[i].style.display = "";
        } else {
          tr[i].style.display = "none";
        }
      }
    }
  }
  
  // Function to start voting for the final game using AJAX
  function startVoting(gameId) {
    fetch(`/admin/game/${gameId}/start_voting`, {
      method: 'POST'
    })
    .then(response => response.text())
    .then(result => {
      console.log(result);
      // Handle any necessary UI updates on the admin side
    })
    .catch(error => {
      console.error('Error starting voting:', error);
    });
  }

  
  
  // Event Listeners for forms and buttons
  document.addEventListener('DOMContentLoaded', () => {
    // Update player score forms
    const updateScoreForms = document.querySelectorAll('.update-score-form');
    updateScoreForms.forEach(form => {
      form.addEventListener('submit', (event) => {
        event.preventDefault();
        const playerId = form.querySelector('[name="player_id"]').value;
        const points = parseInt(form.querySelector('[name="points"]').value);
        updatePlayerScore(playerId, points);
      });
    });
  
    // Update team score forms
    const updateTeamScoreForms = document.querySelectorAll('.update-team-score-form');
    updateTeamScoreForms.forEach(form => {
      form.addEventListener('submit', (event) => {
        event.preventDefault();
        const teamId = form.querySelector('[name="team_id"]').value;
        const points = parseInt(form.querySelector('[name="points"]').value);
        updateTeamScore(teamId, points);
      });
    });
  
    // Eliminate player forms
    const eliminatePlayerForms = document.querySelectorAll('.eliminate-player-form');
    eliminatePlayerForms.forEach(form => {
      form.addEventListener('submit', (event) => {
        event.preventDefault();
        const playerId = form.querySelector('[name="player_id"]').value;
        const gameId = form.querySelector('[name="game_id"]').value;
        const action = form.querySelector('[name="action"]').value; // Get the action from the hidden field
        eliminatePlayer(playerId, gameId, action);
      });
    });




    const gameControlButtons = document.querySelectorAll('.game-control-button');
    gameControlButtons.forEach(button => {
      button.addEventListener('click', () => {
        const gameId = button.dataset.gameId;
        const action = button.dataset.action;
  
        if (action === 'reveal') {
          revealGame(gameId);
        } else if (action === 'complete') {
          completeGame(gameId);
        } else if (action === 'start_voting') {
          startVoting(gameId);
        } else if (action === 'restart') {
          restartGame(gameId);
        }
      });
    });

    const deletePlayerForms = document.querySelectorAll('.delete-player-form');
  deletePlayerForms.forEach(form => {
    form.addEventListener('submit', (event) => {
      event.preventDefault();
      const playerId = parseInt(form.action.split('/').pop());
      
      if (confirm('Are you sure you want to delete this player? This action cannot be undone.')) {
        fetch(form.action, {
          method: 'POST'
        })
        .then(response => {
          if (response.ok) {
            // Remove player row from table
            const playerRow = document.getElementById(`player-row-${playerId}`);
            if (playerRow) {
              playerRow.remove();
            }
          } else {
            throw new Error('Failed to delete player');
          }
        })
        .catch(error => {
          console.error('Error deleting player:', error);
          alert('Error deleting player. Check console for details.');
        });
      }
    });

});

    // Delete game forms
    const deleteGameForms = document.querySelectorAll('form[action^="/admin/delete_game/"]');
    deleteGameForms.forEach(form => {
      form.addEventListener('submit', (event) => {
        event.preventDefault();
        const gameId = parseInt(form.action.split('/').pop());
        deleteGame(gameId);
      });
    });

    
  });