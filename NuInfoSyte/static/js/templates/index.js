ANIMATION_LIST = []



function addAnimation(resetUponAddition=true){
    let textElement = document.querySelector("#text-input");
    let modeElement = document.querySelector("#mode-input");
    let colorElement = document.querySelector("#color-input");
    ANIMATION_LIST.push({
        "text": textElement.value,
        "mode": modeElement.value,
        "color": colorElement.value,
    });
    if(resetUponAddition){
        textElement.value = "";
        modeElement.value = "automode";
        colorElement.value = "autocolor";
    }
    updateAnimationDisplayTable();
}

function tableRowClickHandler(event) {
    /**
     * Click handler for animation list rows
     * Removes animation on click
     */
    let element = event.target;
    // Td ->
    element = element.parentNode;
    if(element.tagName !== "TR") {
        console.error("Could not find proper table row element...");
        return;
    }
    let countTd = element.getElementsByClassName("table-count-section-entry")[0];
    let textTd = element.getElementsByClassName("table-text-section-entry")[0];
    let modeTd = element.getElementsByClassName("table-mode-section-entry")[0];
    let colorTd = element.getElementsByClassName("table-color-section-entry")[0];
    ANIMATION_LIST.splice(parseInt(countTd.innerHTML), 1);
    element.remove();
    updateAnimationDisplayTable();
}

function sendAnimations() {
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

function addItemToAnimationDisplayTable(index, text, mode, color,
                                        tbody=document.querySelector("#animation-list-display > table > tbody")){
    let tableRow = document.createElement("tr");
    tableRow.addEventListener("click", tableRowClickHandler);
    let count = document.createElement("th");
    count.className = "table-count-section-entry";
    let textTd = document.createElement("td");
    textTd.className = "table-text-section-entry";
    let modeTd = document.createElement("td");
    modeTd.className = "table-mode-section-entry";
    let colorTd = document.createElement("td");
    colorTd.className = "table-color-section-entry";
    count.innerHTML = index;
    count.scope = "row";
    textTd.innerHTML = text;
    modeTd.innerHTML = mode;
    colorTd.innerHTML = color;
    tableRow.appendChild(count);
    tableRow.appendChild(textTd);
    tableRow.appendChild(modeTd);
    tableRow.appendChild(colorTd);
    tbody.appendChild(tableRow);
}
function updateAnimationDisplayTable(){
    let tbody = document.querySelector("#animation-list-display > table > tbody");
    removeAllChildNodes(tbody);
    for(item in ANIMATION_LIST){
        addItemToAnimationDisplayTable(item, ANIMATION_LIST[item].text, ANIMATION_LIST[item].mode,
                                       ANIMATION_LIST[item].color, tbody);
    }
}