function countdownThenRedirect(durationSeconds, redirectLink){
    let startTime = Date.now() / 1000;
    let countdownIntElement = document.querySelector("#countdown-integer");
    let intid = setInterval(()=>{
        let currentTime = Date.now() / 1000;
        if(currentTime-startTime >= durationSeconds){
            // Get pathname from any url, whether it has a dc
            let redirectLinkPath = '/'+ redirectLink.replace(/https:\/\/|http:\/\//g,"").split('/').slice(1).join('/');
            // If we are trying to relocate to the same path, something is probably wrong, so we go home
            window.location.href = window.location.pathname != redirectLinkPath ? redirectLink : "/";
            clearInterval(intid);
        }
        countdownIntElement.innerHTML = (durationSeconds - Math.round((currentTime-startTime))).toString();
    }, 0);
}

function main(){
    let countdownDuration = Number.parseInt(document.currentScript.getAttribute("data-countdown-duration"));
    let redirectLink = document.currentScript.getAttribute("data-redirect-link");
    if (countdownDuration){
        //  Wait until we have focus to start the redirect countdown
        if (!document.hasFocus()){
            let focused = () => {
                window.removeEventListener("focus", focused);
                countdownThenRedirect(countdownDuration, redirectLink);
            }
            window.addEventListener("focus", focused);
        }
        else {
            countdownThenRedirect(countdownDuration, redirectLink);
        }
    }
}

main();