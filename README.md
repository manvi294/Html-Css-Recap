const chat = document.querySelector('.webchat__basic-transcript');

  chat.addEventListener('webchatincomingactivities', () => {
    // Select the CSAT question container
    const csatQuestionContainer = document.querySelector('.webchat__csat-question');

    // Select the stars and apply CSS to decrease their size
    const stars = csatQuestionContainer.querySelectorAll('.webchat__csat-question__rating-icon');
    stars.forEach(star => {
      star.style.fontSize = '10px'; // Adjust the value as needed to decrease the size of the stars
    }