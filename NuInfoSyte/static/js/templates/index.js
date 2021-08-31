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
        console.log(ANIMATION_LIST);
}

function removeAllChildNodes(parent) {
    while (parent.firstChild) {
        parent.removeChild(parent.firstChild);
    }
}

function addItemToAnimationDisplayTable(index, text, mode, color, position,
                                        tbody=document.querySelector("#animation-list-display > table > tbody")){
    let tableRow = document.createElement("tr");
    let enumeration = document.createElement("th");
    let textTd = document.createElement("td");
    let modeTd = document.createElement("td");
    let colorTd = document.createElement("td");
    let positionTd = document.createElement("td");
    enumeration.innerHTML = index;
    enumeration.scope = "row";
    textTd.innerHTML = text;
    modeTd.innerHTML = mode;
    colorTd.innerHTML = color;
    positionTd.innerHTML = position;
    tableRow.appendChild(enumeration);
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