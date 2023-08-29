function createSquare(className, backgroundColor) {
    const square = document.createElement('div');
    square.className = className;
    square.style.width = '75px';
    square.style.height = '50px';
    square.style.backgroundColor = backgroundColor;
    return square;
  }
  
  function toggleLightsAB() {
    lightA = !lightA;
    lightB = !lightB;
    squareA.style.backgroundColor = lightA ? 'black' : 'blue';
    squareB.style.backgroundColor = lightB ? 'black' : 'blue';
  }
  
  function toggleLightsBC() {
    lightB = !lightB;
    lightC = !lightC;
  
    squareB.style.backgroundColor = lightB ? 'black' : 'blue';
    squareC.style.backgroundColor = lightC ? 'black' : 'blue';
  }
  
  const app = document.querySelector('.app');
  const squareA = createSquare('square', 'blue');
  const squareB = createSquare('square', 'blue');
  const squareC = createSquare('square', 'blue');
  app.appendChild(squareA);
  app.appendChild(squareB);
  app.appendChild(squareC);
  
  let lightA = false;
  let lightB = false;
  let lightC = false;
  
  const buttonAB = document.createElement('button');
  buttonAB.textContent = 'Toggle A & B';
  buttonAB.addEventListener('click', toggleLightsAB);
  app.appendChild(buttonAB);
  
  const buttonBC = document.createElement('button');
  buttonBC.textContent = 'Toggle B & C';
  buttonBC.addEventListener('click', toggleLightsBC);
  app.appendChild(buttonBC);
  