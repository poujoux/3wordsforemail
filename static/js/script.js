let imgflg = false; //Prevents another image selection during an ongoing process
let uplflg = false; //Prevents another messages of sending during an ongoing process

let idinterval = null; //The setInterval id of the checkInterval
let tintervalid = null; // The setInterval id of the time function

let formemail = null;


window.onload = function(){

    //it cuts the process even after it is reloaded 
    if(formemail){
        formemail.reset();
    }  
       
    [idinterval, tintervalid] = intcleaner(idinterval,tintervalid);

};

function intcleaner(idint, tidint){
    if(idint){
        clearInterval(idint);
    }
    if(tidint){
        clearInterval(tidint);
    }


    return [null, null];
}

let setattr = function(item, index){
    item.style.opacity = "0.5";
    item.style.border = "2px solid black";

    item.style.width = item.offsetWidth*0.8+"px";
    item.style.height = item.offsetHeight*0.8+"px";

    item.setAttribute("imgon", "true");
    item.setAttribute("number", index);

};


document.addEventListener("DOMContentLoaded", () => {
    
    formemail = document.getElementById("femail");

    let imgs = document.querySelectorAll("#imgs > img");
        imgs.forEach((item, index) => {

            item.onclick = function(){
                    if (uplflg) {
                        return;
                    }
                if(!imgflg){                    
                    setattr(item, index);

                    imgflg=item;
                }
                else{
                    imgflg.removeAttribute("style");
                    imgflg.removeAttribute("number");
                    imgflg.removeAttribute("imgon");

                    if(imgflg!==item || item.hasAttribute("lll")){
                        setattr(item, index);
                        item.removeAttribute("lll");

                    }
                    else if(imgflg===item){
                        item.setAttribute("lll", false);
                    }

                    imgflg = item;
                }
            };

        });
});

function timer(time){

    const cnf = document.createElement("div");
    cnf.className = "timdiv";

    const timtext = document.createElement("a");
    const a = document.createElement("br");
    const tmr = document.createElement("timer");

    cnf.appendChild(timtext);
    cnf.appendChild(a);
    cnf.appendChild(tmr);

    timtext.innerText = "Waiting to confirm it...";


    let t = time;
    document.body.appendChild(cnf);

    tintervalid = setInterval(() => {

        tmr.innerText = t;
        t--;

        if(t === 0){
            alert("The subscription has not been confirmed")
            cnf.remove();

            [idinterval, tintervalid] = intcleaner(idinterval,tintervalid);
        }
    }, 1000);
    return cnf;
}

let checkinterval = function(text, tcnf) {
    idinterval = setInterval(() => {
        fetch("/")
            .then(response => response.json())
            .then(data => {
                if (data.Status === "A") {
                    alert("It is confirmed!");

                    if(tcnf){
                        tcnf.remove();
                    } 
                    

                    [idinterval, tintervalid] = intcleaner(idinterval,tintervalid);
                    showdb(text);

                    uplflg = false;

                }
            })
            .catch(error => {
                console.error("An error occurred:" + (error.message || "Undefined error"));
            });
    }, 8000);
};


function showdb(text){
    fetch(`/dysend?q=${text}`)
        .then(response => {
            if(!response.ok){
                return response.json().then(data => {
                    throw Error(data.message);})}

            return response.json(); })
        .then(data => {

            list = document.createElement("p");
            list.className="listtext";

            list.innerText = "No sended elements";

            if(data["Items"]){

            list.innerText = `The ${data["Items"].length} last sended elements`;

            ull = document.createElement("ul");
            ull.className="listtext";


            data["Items"].forEach(item => {
                li = document.createElement("li");
                li.innerText = item;
                ull.appendChild(li);
            });
            document.body.appendChild(ull);


            }
            document.body.appendChild(list);


        })
        .catch(error => {
            alert("An error occurred: " + (error.message || "Unknown error"));
            console.log("An error occurred", error.message);
            alert("An error occurred: " + (error.message || "Unknown error"));
    });

}


document.addEventListener("submit", function(event) {
    event.preventDefault();

    if (uplflg) {
        alert("Form is already being processed.");
        return;
    }


    uplflg = true;

    const form = new FormData(event.target);
    let text = form.get("textf");


    if (!(text && text.includes(" ") && text.split(" ").length === 3 && !(text.split(" ").some(item => !item)) )) {

        if(text && text.replace(/\s+/g, "").length === 3 && text.length - text.replace(/\s+/g, "").length > 2){

            alert("There are extra spaces in the text");
    
    }

        alert("Please enter a valid statement.");
        uplflg = false;
        return;  
    }
    
    else{
        var uplflgnum = imgflg ? imgflg.getAttribute("number") : null;
        text = uplflgnum ? `${text}&a=${uplflgnum}` : text;
    }


    const ul = document.querySelector("ul.listtext");
    const list = document.querySelector("p.listtext");
    
    const txt = document.querySelector("span.smpletxt");
    const br = document.querySelector("br.smpletxt");

    let tcnf = document.querySelector(".timdiv");

    [idinterval, tintervalid] = intcleaner(idinterval,tintervalid);
    
   
    if (tcnf){
        tcnf.remove();
    }


    if(ul && list){
        ul.remove();
        list.remove();
    }
    if(txt || br){
        txt.style.display = "none";
        br.style.display = "none";
    }

    
    fetch(event.target.action, {
        method: "POST",
        body: form
    })
    .then(response => {
        if(!response.ok){
            return response.json().then(data => {
                throw new Error(data.message || "Unknown error");
            })
        }
        
        return response.json();
    })
    .then(data => {
        if (data.Status === "F") {
            console.log("Waiting to confirm it...");

            tcnf = timer(60);

            checkinterval(text, tcnf);

            uplflg = false;

        }
        else if(data.Status === "A"){
            console.log("It is the same email.");
            showdb(text);
            uplflg = false;


        }
        
    })
    .catch(error => {
        alert("An error occurred: " + (error.message || "Unknown error"));
        console.error("An error occurred: " + (error.message || "Unknown error"));
        uplflg = false;

    })
    
});

