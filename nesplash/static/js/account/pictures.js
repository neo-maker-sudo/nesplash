
const li = document.getElementsByClassName("account-2-a")[1]
const picture_section = document.getElementById("picture-section-2");
const photo_id = document.getElementsByClassName("picture-section-2-div");
const btns = document.getElementsByClassName("picture-delete-button");

li.classList.add("select");

let page = 0;
let post_flag = false;

class Account {
    // delete personal photo function
    delete_personal_photoData(){
        for(let i=0;i<photo_id.length;i++){
            btns[i].onclick = ()=>{
                const url = `${window.port}/api/user/delete-public-image`
                fetch(url,{
                    method: 'POST',
                    body: JSON.stringify({
                        id: photo_id[i].id
                    }),
                    headers: {
                        "Content-Type": "application/json"
                    }
                })
                .then( async ( response )=>{
                    return await response.json()
                })
                .then((result)=>{
                    if(result.ok == true){
                        window.location.reload()
                    }
                    else if(result.error == "none exist photo"){
                        alert("刪除照片異常，請聯繫管理員 eyywqkgb@gmail.com")
                    }
                })
            }
        }
    }

    // display personal photo function
    display_personal_photoData(results){

        for(let i=0;i<results.length;i++){
            const div = document.createElement("div");
            const img = document.createElement("img");
            const label = document.createElement("label");
            const p = document.createElement("p");
            const h4 = document.createElement("h4");
            const button = document.createElement("button");
            const div_2 = document.createElement("div");

            picture_section.appendChild(div);
            div.appendChild(div_2);
            div_2.appendChild(h4);
            div_2.appendChild(button);
            div.appendChild(img);
            div.appendChild(label)
            div.appendChild(p);
            

            const date = new Date(results[i].timestamp)
            h4.textContent = `${date.toGMTString()}`;
            div_2.classList.add("picture-section-2-topDiv");
            div.classList.add("picture-section-2-div");
            div.setAttribute("id", `${results[i].id}`)
            img.classList.add("picture-section-2-img");
            img.setAttribute("src", `${results[i].imageurl}`);
            label.classList.add("picture-label");
            
            if(`${results[i].label}` == "" || `${results[i].label}` == undefined){
                label.textContent = "";
            }else{
                label.textContent = `${results[i].label}`;
            }

            p.textContent = `${results[i].description}`;
            button.textContent = "Delete";
            button.classList.add("picture-delete-button");
        }
        this.delete_personal_photoData()
    }

    // fetch api
    fetchData(page){
        if(post_flag) {
            return;
        };
        const url = `${window.port}/api/user/personal-photos?page=${page}`;
        post_flag = true
        fetch(url)
        .then( async ( response )=>{
            const data = await response.json()
            post_flag = false
            return data
        })
        .then(( result )=>{
            this.display_personal_photoData(result.message)
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