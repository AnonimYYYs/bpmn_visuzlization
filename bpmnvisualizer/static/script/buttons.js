// --- --- adding buttons canvas --- ---
const buttonApp = document.createElement("div");
document.body.appendChild(buttonApp);


function createButton(buttonText, style, onClickFunction){
    var button = document.createElement("button");
    button.classList.add("btn");
    button.classList.add("model-button");
    button.classList.add(style);
    button.innerHTML = buttonText;
    button.onclick = onClickFunction
    return button
}


// --- >>> input N <<< ---
var inputN = document.createElement('input');
inputN.type = "text";
inputN.size = 5
inputN.placeholder = "1";
inputN.classList.add("model-button");
buttonApp.appendChild(inputN);


// --- >>> make step button <<< ---
// function on button click
function onStepButtonUp() {
  makeStepRequest();
}

// make request to backend server
function makeStepRequest() {
  // MOST SIMPLE ONE
  fetch(getUrlStep(parseInt(inputN.value)))
  .then(response => response.json())
  .then( json => {
    let i = 0;
    while (i < Object.keys(json).length){
      makeStep(json[`${i}`]);
      i += 1;
    }
  })
  .catch(error => console.error(error))
}

const buttonStep = createButton(buttonStepText, "btn-success", onStepButtonUp);
buttonApp.appendChild(buttonStep);


// --- >>> reset model button <<< ---
// function on button click
function onResetButtonUp() {
    resetAll = true;
    makeResetRequest();
}

// make request to backend server
function makeResetRequest() {
  // MOST SIMPLE ONE
  fetch(URLRESET)
  .catch(error => console.error(error))
}

const buttonReset = createButton(buttonResetText, "btn-secondary", onResetButtonUp);
buttonApp.appendChild(buttonReset);


// --- >>> input model name <<< ---
//var inputName = document.createElement('input');
//inputName.type = "text";
//inputName.size = 20
//inputName.placeholder = "new model name";
//inputName.classList.add("model-button");
//buttonApp.appendChild(inputName);



var theHTMLToInsert = `
<select name="model-dropout-names" id="model-dropout-names">
  <option value="ring">кольцо строповочное</option>
  <option value="kron">кронштейн</option>
  <option value="kronturn">кронштейн поворотный</option>
  <option value="finger">палец</option>
  <option value="plate">плита</option>
  <option value="trap">трапеция</option>
</select>`;

buttonApp.insertAdjacentHTML("beforeend", theHTMLToInsert);


// --- >>> new model button <<< ---
// function on button click
function onModelButtonUp() {
    var e = document.getElementById("model-dropout-names");
//    alert(e.options[e.selectedIndex].text);
    generateNewCanvas(e.options[e.selectedIndex].text);
}

const buttonModel = createButton(buttonModelText, "btn-secondary", onModelButtonUp);
buttonApp.appendChild(buttonModel);



// --- >>> new model button <<< ---
// function on button click
function onStatsButtonUp() {
    stats();
}

const buttonStats = createButton(buttonStatsText, "btn-info", onStatsButtonUp);
buttonApp.appendChild(buttonStats);
