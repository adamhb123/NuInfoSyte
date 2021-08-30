ANIMATION_LIST = []



function addAnimation(resetUponAddition=true){
    console.log("BRUH");
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
    console.log(ANIMATION_LIST);
    updateAnimationDisplayTable();
}



function updateAnimationDisplayTable(){
    let table = document.querySelector("#animation-list-display");
    for(item in ANIMATION_LIST){
    // TODO: erase existing table rows (except header)
        console.log(item);
        let tableRow = document.createElement("tr");
        let textTd = document.createElement("td");
        let modeTd = document.createElement("td");
        let colorTd = document.createElement("td");
        let positionTd = document.createElement("td");
        textTd.innerHTML = ANIMATION_LIST[item].text;
        modeTd.innerHTML = ANIMATION_LIST[item].mode;
        colorTd.innerHTML = ANIMATION_LIST[item].color;
        positionTd.innerHTML = ANIMATION_LIST[item].position;
        tableRow.appendChild(textTd);
        tableRow.appendChild(modeTd);
        tableRow.appendChild(colorTd);
        tableRow.appendChild(positionTd);
        table.appendChild(tableRow);
    }
}