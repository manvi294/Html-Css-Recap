// Inject custom CSS to adjust the size of the stars
const styleNode = document.createElement('style');
styleNode.innerHTML = `
  .webchat__csat-question__rating-icon {
    font-size: 10px; /* Adjust the value as needed to decrease the size of the stars */
  }
`;
document.head.appendChild(styleNode);