
const li = document.getElementsByClassName("account-2-a")[2]
const collection_section = document.getElementById("collect-section-2");

li.classList.add("select");

var page = 0;
var post_flag = false;

class Account {
    // display personal collection photos function
    display_collection_photoData(results){
        for(var i=0;i<results.length;i++){
            const div = document.createElement("div");
            const img = document.createElement("img");
            const label = document.createElement("label");
            const p = document.createElement("p");
            const h4 = document.createElement("h4");

            collection_section.appendChild(div);
            div.appendChild(h4)
            div.appendChild(img);
            div.appendChild(label);
            div.appendChild(p);

            h4.textContent = `${results[i].timestamp}`;
            div.classList.add("collect-section-2-div");
            img.classList.add("collect-section-2-img");

            if(`${results[i].label}` == "" || `${results[i].label}` == undefined){
                label.textContent = "";
            }else{
                label.textContent = `${results[i].label}`;
            }
            
            if(results[i].imageurl.split(".")[1] == "cloudfront"){
                img.setAttribute("src", `${results[i].imageurl}`);
            }
            else{
                img.setAttribute("src", `${results[i].imageurl}` + "&w=500&h=300&dpr=2");
            }
            
            p.textContent = `${results[i].description}`;
        }
    }
    // fetch api
    fetchData(page){
        if(post_flag) {
            return;
        };
        const url = `${window.port}/api/user/collect-photos?page=${page}`;
        post_flag = true
        fetch(url)
        .then( async ( response )=>{
            const data = await response.json()
            post_flag = false
            return data
        })
        .then(( result )=>{
            this.display_collection_photoData(result.message)
            window.onscroll = () => {
                if(result.nextPage != null){
                    if(window.innerHeight + window.scrollY >= document.documentElement.scrollHeight - 100){
                        this.fetchData(result.nextPage)
                    } 
                }
            }
        })
    }
}


document.addEventListener("DOMContentLoaded", ()=>{
    const account = new Account
    account.fetchData(page)
})