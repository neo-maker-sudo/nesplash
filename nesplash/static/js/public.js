const public_section_2 = document.getElementById("public-section-2");
const public_section_1 = document.querySelector(".public-section-1");

var page = 0;
var post_flag = false;
const user_id = location.pathname.split("/")[2]

class Public {
    // display follow status
    getFollowStatus(){
        const follow_btn = document.querySelector(".public-follow");
        const url = `${window.port}/api/is_following_or_not/${user_id}`;
        fetch(url)
        .then( async ( response )=>{
            return await response.json()
        })
        .then(( result )=>{
            if(result.message == "match"){
                follow_btn.style.background = "#CCCCCC";
                follow_btn.style.color = "black";
                follow_btn.textContent = "Already followed"
            }
            else if(result.message == "nomatch"){
                follow_btn.style.background = "transparent";
                follow_btn.style.color = "black";
            }
        })
    }
    // follow and unfollow
    followUser(){
        const follow_btn = document.querySelector(".public-follow");
        follow_btn.onclick = ()=>{
            if(follow_btn.style.background !== "rgb(204, 204, 204)"){
                const url = `${window.port}/api/follow/${user_id}`
                fetch(url)
                .then( async ( response )=>{
                    return await response.json()
                })
                .then(( result )=>{
                    console.log(result)
                    if(result.ok == true){
                        window.location.reload()
                    }
                    else if(result.error == "you have to login first"){
                        location.href = `${window.port}` + "/signin"
                    }
                    else if(result.error == "none exist user"){
                        alert("無此使用者")
                    }
                })
            }
            else {
                const url = `${window.port}/api/unfollow/${user_id}`
                fetch(url)
                .then( async ( response )=>{
                    return await response.json()
                })
                .then(( result )=>{
                    if(result.ok == true){
                        window.location.reload()
                    }
                    else if(result.error == "you have to login first"){
                        location.href = `${window.port}` + "/signin"
                    }
                    else if(result.error == "none exist user"){
                        alert("無此使用者")
                    }
                })
            }
        }
    }
    // display user data
    display_public_userData(result){
        const div = document.createElement("div");
        const div_2 = document.createElement("div");
        const s_div_1 = document.createElement("div");
        const s_div_2 = document.createElement("div");
        const n_div_1 = document.createElement("div");
        const img = document.createElement("img");
        const name = document.createElement("h3");
        const bio = document.createElement("p");
        const link = document.createElement("a");
        const location = document.createElement("h3");
        const follow = document.createElement("button");
        const span_photo = document.createElement("span")
        const span_collection = document.createElement("span");

        public_section_1.appendChild(div);
        public_section_1.appendChild(div_2);
        div.appendChild(s_div_1);
        div.appendChild(s_div_2);
        s_div_1.appendChild(img);
        s_div_2.appendChild(n_div_1);
        n_div_1.appendChild(name);
        n_div_1.appendChild(follow);
        s_div_2.appendChild(link);
        s_div_2.appendChild(location);
        s_div_2.appendChild(bio);

        div_2.appendChild(span_photo);
        div_2.appendChild(span_collection);

        div.classList.add("public-topDiv");
        div_2.classList.add("public-botDiv");
        s_div_1.classList.add("public-imageDiv");
        s_div_2.classList.add("public-infoDiv");

        if(result.profile_image.split(".")[1] == "jpg"){
            img.setAttribute("src", `/static/profile_pics/${result.profile_image}`)
        }
        else if(result.profile_image.split(".")[1] == "png"){
            img.setAttribute("src", `/static/profile_pics/${result.profile_image}`)
        }
        else{
            img.setAttribute("src", `${result.profile_image}`);
        }

        n_div_1.classList.add("public-nameDiv")
        img.classList.add("public_image_profile");
        name.classList.add("public_name");
        name.textContent = `${result.username}`;
        
        follow.textContent = `Follow`
        follow.classList.add("public-follow");
        

        if (result.link == null){
            link.textContent = "No Link";
            link.classList.add("public-nolink");
        }
        else{
            
            if(result.link.split(".")[0] === "www"){
                link.textContent = "Website";
                link.setAttribute("href", `https://${result.link}`);
            }else{
                link.textContent = "Unsplash";
                link.setAttribute("href", `${result.link}`);
            }
            
            link.setAttribute("target", "_blank")
            link.classList.add("public-link");
        }

        location.classList.add("public-location");
        location.textContent = `${result.location}`;
        bio.classList.add("public-bio")
        bio.textContent = `${result.bio}` ? `${result.bio}`: "";

        span_photo.textContent = `${result.total_photos}`;
        span_photo.classList.add("public-spanPhoto");
        span_collection.classList.add("public-spanCollection");
        span_collection.textContent = `${result.total_collections}`;

        this.followUser()
        this.getFollowStatus()
    }
    // display photos data
    display_public_photoData(results){
        
        if(results == undefined){
            const div = document.createElement("div");
            const h1 = document.createElement("h1");

            public_section_2.appendChild(div);
            div.appendChild(h1);

            div.classList.add("public-no-section-2-div");
            h1.textContent = "This User not post any photos yet"
            return;
        }
        for(var i=0;i<results.length;i++){
            const div = document.createElement("div");
            const img = document.createElement("img");
            const dp = document.createElement("p");
            const h3 = document.createElement("h3");

            public_section_2.appendChild(div);
            div.appendChild(h3);
            div.appendChild(img);
            div.appendChild(dp);

            h3.textContent = `${results[i].timestamp}`;
            div.classList.add("public-section-2-div");
            img.classList.add("public-section-2-img");
            img.setAttribute("id", `${results[i].id}`)
            dp.textContent = `${results[i].description}`;

            if(results[i].imageUrl.split(".")[1] == "cloudfront"){
                img.setAttribute("src", `${results[i].imageUrl}`);
            }
            else{
                img.setAttribute("src", `${results[i].imageUrl}` + "&w=500&h=300&dpr=2");
            }
        }
    }
    // fetch api
    fetchData(page){
        if(post_flag) {
            return;
        };
        const url = `${window.port}/api/public/${user_id}?page=${page}`;
        post_flag = true;

        fetch(url)
        .then( async ( response )=>{
            const data = await response.json()
            post_flag = false
            return data
        })
        .then(( result )=>{
            this.display_public_photoData(result.message)
            if (page == 0){
                this.display_public_userData(result.user)
            }            
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

document.addEventListener("DOMContentLoaded", async ()=>{
    const public = new Public
    await public.fetchData(page)
    
})