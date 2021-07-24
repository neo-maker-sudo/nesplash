const section_2 = document.querySelector(".nature-section-2");
const a = document.getElementsByClassName("nature-a")[0];
const photos_id = document.getElementsByClassName("nature-section-2-div");
const icons = document.getElementsByClassName("nature-collect-icon");
const hearts_1 = document.getElementsByClassName("heart1");
const hearts_2 = document.getElementsByClassName("heart2");

var page = 0;
let post_flag = false

class Nature {
    // collect and uncollect api
    heartClick(){
        for(let i=0;i<photos_id.length;i++){
            icons[i].onclick = ()=>{
                if(hearts_1[i].style.background == "red" && hearts_2[i].style.background == "red"){
                    const url = `${window.port}/api/uncollect/${photos_id[i].id}`
                    fetch(url)
                    .then( async ( response )=>{
                        return await response.json()
                    })
                    .then(( result )=>{
                        if(result.ok == true){
                            hearts_1[i].style.background = "#ddd";
                            hearts_2[i].style.background = "#ddd";
                        }else if(result.error == "you have to login first"){
                            location.href = `${window.port}` + "/signin"
                        }
                        else if(result.error == "not exist photo"){
                            alert("not exist photo")
                        }
                    })
                }else{
                    const url = `${window.port}/api/collect/${photos_id[i].id}`
                    fetch(url)
                    .then( async ( response )=>{
                        return await response.json()
                    })
                    .then(( result )=>{
                        if(result.ok == true){
                            hearts_1[i].style.background = "red";
                            hearts_2[i].style.background = "red";
                        }else if(result.error == "you have to login first"){
                            location.href = `${window.port}` + "/signin"
                        }else if(result.error == "not exist photo"){
                            alert("not exist photo")
                        }
                    })
                }
            }
        }   
    }
    // display function
    display_nature(results){
        a.style.color = "blue";
        for(var i=0;i<results.length;i++){
            const div = document.createElement("div");
            const link_div = document.createElement("div");
            const inside_a = document.createElement("a");
            const outside_a = document.createElement("a");
            const s_div = document.createElement("div");
            const s_img = document.createElement("img");
            const img = document.createElement("img");
            const label = document.createElement("label");
            const p = document.createElement("p");
            const download = document.createElement("a");
            const icon = document.createElement("div");
            const iconDiv_1 = document.createElement("div");
            const iconDiv_2 = document.createElement("div");

            section_2.appendChild(div);
            div.appendChild(s_div);
            s_div.appendChild(s_img);
            s_div.appendChild(link_div);
            link_div.appendChild(inside_a);
            link_div.appendChild(outside_a);
            s_div.appendChild(icon);
            icon.appendChild(iconDiv_1);
            icon.appendChild(iconDiv_2);
            s_div.appendChild(download);
            div.appendChild(img);
            div.appendChild(label);
            div.appendChild(p);

            div.classList.add("nature-section-2-div");
            img.classList.add("nature-section-2-img");
            s_img.classList.add("sec_2_imgfile");
            s_div.classList.add("sec_2_topDiv");
            link_div.classList.add("nature-link-div");
            inside_a.classList.add("nature-section-2-inside-a");
            outside_a.classList.add("nature-section-2-outside-a");
            p.classList.add("nature-section-2-p");
            icon.classList.add("nature-collect-icon");
            download.classList.add("nature-sec_2_download");
            iconDiv_1.classList.add("heart1");
            iconDiv_2.classList.add("heart2");
            
            if(results[i].imageurl.split(".")[1] == "cloudfront"){
                img.setAttribute("src", `${results[i].imageurl}`)
            }
            else{
                img.setAttribute("src", `${results[i].imageurl}` + "&w=500&h=300&dpr=2");
            }
            
            div.setAttribute("id", `${results[i].id}`);
            s_img.setAttribute("src", `${results[i].profile_image}`);

            if (results[i].link == null){
                outside_a.textContent = "No Link";
            } else {
                outside_a.setAttribute("href", `${results[i].link}`);
                outside_a.setAttribute("target", "_blank");
                outside_a.textContent = "Website";
            }

            inside_a.textContent = `${results[i].user}` == "" ? "anonymous" : `${results[i].user}`;
            inside_a.setAttribute("href", `/public/${results[i].user_id}`);

            if(`${results[i].label}` == "" || `${results[i].label}` == undefined){
                label.classList.add("label-desc")
                label.textContent = "";
            }else{
                label.classList.add("label-desc")
                label.textContent = `${results[i].label}`;
            }
            
            if(results[i].description == null){
                p.textContent = ""
            } else {
                p.textContent = `${results[i].description}`;
            }
            
            download.setAttribute("target", "_blank");
            download.setAttribute("href", `${results[i].download}` + "?force=true");
            download.setAttribute('download', 'download');
            download.textContent = "Download";
        }
        this.heartClick()
        this.getCollectedData()
    }
    // fetch api
    fetchData(page){
        if(post_flag) {
            return;
        };
        const url = `${window.port}/nature/api/photos?page=${page}`;
        post_flag = true;
        fetch(url)
        .then( async (response)=>{
            const data = await response.json()
            post_flag = false
            return data
        })
        .then((result)=>{
            this.display_nature(result.message)
            window.onscroll = () => {
                if(result.nextPage != null){
                    if(window.innerHeight + window.scrollY >= document.documentElement.scrollHeight - 100){
                        this.fetchData(result.nextPage)
                    } 
                }
            }
        })
    }
    // get collect data to display function
    getCollectedData(){
        const url = `${window.port}/api/collected_photo_id`
        fetch(url)
        .then( async ( response )=>{
            return await response.json()
        })
        .then(( result )=>{
            result.message.map((item)=>{
                for(let i=0;i<photos_id.length;i++){
                    if(photos_id[i] !== undefined){
                        if(photos_id[i].id == item){
                            hearts_1[i].style.background = "red";
                            hearts_2[i].style.background = "red";
                        }
                    }
                }
            })
        })
    }
}

document.addEventListener("DOMContentLoaded", ()=>{
    const nature = new Nature
    nature.fetchData(page)
})