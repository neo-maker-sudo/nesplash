const section_2 = document.getElementById("main-section-2");
const photos_id = document.getElementsByClassName("main-section-2-div");
const icons = document.getElementsByClassName("main-collect-icon");
const hearts_1 = document.getElementsByClassName("heart1");
const hearts_2 = document.getElementsByClassName("heart2");
const search = document.querySelector(".section-1-searchBox");


const search_photos = document.getElementById("search-photos");
const search_users = document.getElementById("search-users");
const search_label = document.getElementById("search-label");

const keywordLi = document.getElementsByClassName("search-keyword");

var page = 0;
var post_flag = false;
let index = 0;

class Main {
    // for function for display
    for_function(results){
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

            div.classList.add("main-section-2-div");
            img.classList.add("main-section-2-img");
            label.classList.add("main-label");
            s_img.classList.add("sec_2_imgfile");
            s_div.classList.add("sec_2_topDiv");
            link_div.classList.add("main-link-div");
            inside_a.classList.add("main-section-2-inside-a");
            outside_a.classList.add("main-section-2-outside-a");
            p.classList.add("main-section-2-p");
            icon.classList.add("main-collect-icon");
            download.classList.add("main-sec_2_download");
            iconDiv_1.classList.add("heart1");
            iconDiv_2.classList.add("heart2");

            if(results[i].imageurl.split(".")[1] == "cloudfront"){
                img.setAttribute("src", `${results[i].imageurl}`)
            }
            else{
                img.setAttribute("src", `${results[i].imageurl}` + "&w=500&h=300&dpr=2");
            }
            
            s_img.setAttribute("src", `${results[i].User.profile_image}`);
            div.setAttribute("id", `${results[i].id}`);
            outside_a.setAttribute("href", `${results[i].User.link}`);
            outside_a.setAttribute("target", "_blank");
            outside_a.textContent = "Unsplash";
            inside_a.textContent = `${results[i].User.user}`;
            inside_a.setAttribute("href", `/public/${results[i].User.user_id}`);
            
            if(`${results[i].label}` == "" || `${results[i].label}` == undefined){
                label.textContent = "";
            }else{
                label.textContent = `${results[i].label}`;
            }
            
            p.textContent = `${results[i].description}`;
            download.setAttribute("target", "_blank");
            download.setAttribute("href", `${results[i].download}` + "?force=true");
            download.setAttribute('download', 'download');
            download.textContent = "Download";
        }
        this.heartClick()
        this.getCollectedData()
    }
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

    // display search photos function
    async display_search_photos(results){
        await this.removeAttraction()
        this.for_function(results)
    }

    // display search users function
    async display_search_users(results){
        await this.removeAttraction()
        for(var i=0;i<results.length;i++){
            const div = document.createElement("div");
            const link_div = document.createElement("div");
            const inside_a = document.createElement("a");
            const s_div = document.createElement("div");
            const s_img = document.createElement("img");
            const img = document.createElement("img");

            section_2.appendChild(div);
            div.appendChild(s_div);
            s_div.appendChild(link_div);
            s_div.appendChild(s_img);
            link_div.appendChild(inside_a);
            div.appendChild(img);

            div.classList.add("main-section-2-div");
            img.classList.add("main-section-2-img");
            s_img.classList.add("search_2_imgfile");
            s_div.classList.add("search_2_topDiv");
            link_div.classList.add("main-link-div");
            inside_a.classList.add("main-section-2-inside-a");
            
            s_img.setAttribute("src", `${results[i].User.profile_image}`);
            inside_a.textContent = `${results[i].User.user}`;
            inside_a.setAttribute("href", `/public/${results[i].User.user_id}`);
            inside_a.setAttribute("target", "_blank")
        }
    }
    // display no data after search
    display_no_data(){
        const div = document.createElement("div");
        const h3 = document.createElement("h3");

        section_2.appendChild(div);
        div.appendChild(h3);
        div.classList.add("main-no-data")
        h3.textContent = "dont have any data according to your keyword search"
    }

    // remove display data
    removeAttraction(){
        while(section_2.hasChildNodes()){
            section_2.removeChild(section_2.firstChild)
        }
    }

    // users(){
    //     search_users.onclick = ()=>{
    //         search_photos.style.background = 'white'
    //         search_users.style.background = '#448899'
    //     }
    // }

    // photos(){
    //     search_photos.onclick = ()=>{
    //         search_users.style.background = 'white'
    //         search_photos.style.background = '#448899'
    //     }
    // }

    // switch keyword label
    switch(){
        for(let i=0;i<keywordLi.length;i++){
            keywordLi[i].num = i
            keywordLi[i].onclick = ()=>{
                index = keywordLi[i].num;
                this.labelColor()
            }
        }
    }

    labelColor(){
        for(var i=0;i<keywordLi.length;i++){
            keywordLi[i].style.background = '';
        }
        keywordLi[index].style.background = '#448899'
    }

    // search keyword api for nextpage
    search_nextpage_photos(nextpage, keyword){
        if(post_flag){
            return;
        }
        if(nextpage == null){
            return
        }
        const url = `${window.port}/api/photos/search?page=${nextpage}&q=${keyword}`;
        post_flag = true;
        fetch(url)
        .then( async ( response )=>{
            const data = await response.json()
            post_flag = false;
            return data
        })
        .then((result)=>{
            this.display_section_2(result.message)
            window.onscroll = () => {
                if(result.nextPage != null){
                    if(window.innerHeight + window.scrollY >= document.documentElement.scrollHeight - 100){
                        this.search_nextpage_photos(result.nextPage, keyword)
                    } 
                }
            }
        })
}
    // search keyword api
    search_photos(page){
        search.addEventListener("submit",(e)=>{
            if(post_flag){
                return;
            }
            e.preventDefault()
            const keyword = document.getElementById("section-1-input-keyword").value;
            if(keyword == ""){
                alert("請至少輸入一個欄位的內容作查詢")
            }

            const photoSelected = search_photos.style.background
            const userSelected = search_users.style.background
            const labelSelected = search_label.style.background
            if(photoSelected == "rgb(68, 136, 153)" && userSelected == "" && labelSelected == ""){
                const url = `${window.port}/api/photos/search?page=${page}&q=${keyword}`;
                post_flag = true;
                fetch(url)
                .then( async ( response )=>{
                    const data = await response.json()
                    post_flag = false;
                    return data
                })
                .then((result)=>{
                    if(result.message.length == 0){
                        this.removeAttraction()
                        this.display_no_data()
                        return;
                    }
                    this.display_search_photos(result.message)
                    window.onscroll = () => {
                        if(result.nextPage != null){
                            if(window.innerHeight + window.scrollY >= document.documentElement.scrollHeight - 100){
                                this.search_nextpage_photos(result.nextPage, keyword)
                            } 
                        }
                    }
                })
            }
            else if(userSelected == "rgb(68, 136, 153)" && photoSelected == "" && labelSelected == "") {
                const url = `${window.port}/api/users/search?page=${page}&q=${keyword}`;
                post_flag = true;
                fetch(url)
                .then( async ( response )=>{
                    const data = await response.json()
                    post_flag = false;
                    return data
                })
                .then((result)=>{
                    if(result.message.length == 0){
                        this.removeAttraction()
                        this.display_no_data()
                        return;
                    }
                    this.display_search_users(result.message)
                    window.onscroll = () => {
                        if(result.nextPage != null){
                            if(window.innerHeight + window.scrollY >= document.documentElement.scrollHeight - 100){
                                this.search_nextpage_photos(result.nextPage, keyword)
                            } 
                        }
                    }
                })
            } else if (labelSelected == "rgb(68, 136, 153)" && photoSelected == "" && userSelected == "") {
                const url = `${window.port}/api/labels/search?page=${page}&q=${keyword}`;
                post_flag = true;
                fetch(url)
                .then( async ( response ) =>{
                    const data = response.json()
                    post_flag = false;
                    return data
                })
                .then(( result )=>{
                    if(result.message.length == 0){
                        this.removeAttraction()
                        this.display_no_data()
                        return;
                    }
                    this.display_search_photos(result.message)
                    window.onscroll = () =>{
                        if(result.message != null) {
                            if(window.innerHeight + window.scrollY >= document.documentElement.scrollHeight - 100){
                                this.search_nextpage_photos(result.nextPage, keyword)
                            } 
                        }
                    }
                })
            }
        })
    }
    // display data function
    display_section_2(results){
        this.for_function(results)
    }

    // fetch api
    fetchData(page){
        if(post_flag) {
            return;
        };
        const url = `${window.port}/api/photos?page=${page}`;
        post_flag = true;
        
        fetch(url)
        .then(async(response)=>{
            const data = response.json()
            post_flag = false
            return data
        })
        .then( async (result)=>{
            await this.display_section_2(result.message)
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



document.addEventListener('DOMContentLoaded', async ()=>{
    const main = new Main
    await main.fetchData(page)
    main.search_photos(page)
    main.labelColor()
    main.switch()
})