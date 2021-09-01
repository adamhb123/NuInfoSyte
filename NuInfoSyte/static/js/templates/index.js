ANIMATION_LIST = []



function addAnimation(resetUponAddition=true){
    let textElement = document.querySelector("#text-input");
    let modeElement = document.querySelector("#mode-input");
    let colorElement = document.querySelector("#color-input");
    let positionElement = document.querySelector("#pos-input");
    ANIMATION_LIST.push({
        "text": textElement.value,
        "mode": modeElement.value,
        "color": colorElement.value,
        "position": positionElement.value
    });
    if(resetUponAddition){
        textElement.value = "";
        modeElement.value = "automode";
        colorElement.value = "autocolor";
        positionElement.value = "fill";
    }
    updateAnimationDisplayTable();
}

function sendAnimations(){
    let xhr = new XMLHttpRequest();
    xhr.open("POST", "/", true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify(ANIMATION_LIST));
}

function removeAllChildNodes(parent) {
    while (parent.firstChild) {
        parent.removeChild(parent.firstChild);
    }
}

function addItemToAnimationDisplayTable(index, text, mode, color, position,
                                        tbody=document.querySelector("#animation-list-display > table > tbody")){
    let tableRow = document.createElement("tr");
    let count = document.createElement("th");
    count.className = "table-count-section-entry";
    let textTd = document.createElement("td");
    textTd.className = "table-text-section-entry";
    let modeTd = document.createElement("td");
    modeTd.className = "table-mode-section-entry";
    let colorTd = document.createElement("td");
    colorTd.className = "table-color-section-entry";
    let positionTd = document.createElement("td");
    positionTd.className = "table-position-section-entry";
    count.innerHTML = index;
    count.scope = "row";
    textTd.innerHTML = text;
    modeTd.innerHTML = mode;
    colorTd.innerHTML = color;
    positionTd.innerHTML = position;
    tableRow.appendChild(count);
    tableRow.appendChild(textTd);
    tableRow.appendChild(modeTd);
    tableRow.appendChild(colorTd);
    tableRow.appendChild(positionTd);
    tbody.appendChild(tableRow);
}
function updateAnimationDisplayTable(){
    let tbody = document.querySelector("#animation-list-display > table > tbody");
    removeAllChildNodes(tbody);
    for(item in ANIMATION_LIST){
        addItemToAnimationDisplayTable(item, ANIMATION_LIST[item].text, ANIMATION_LIST[item].mode,
                                       ANIMATION_LIST[item].color, ANIMATION_LIST[item].position,
                                       tbody);
    }
}