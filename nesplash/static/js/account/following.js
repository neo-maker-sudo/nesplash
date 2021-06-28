
const li = document.getElementsByClassName("account-2-a")[3];
const section_2 = document.getElementById("following-section-2");

let page = 0
let post_flag = false;

class Account {
    // display been followed users function
    display_following(results){
        li.classList.add("select");
        for(var i=0;i<results.length;i++){
            const img = document.createElement("img");
            const div = document.createElement("div");
            const s_div = document.createElement("div");
            const link_div = document.createElement("div");
            const p = document.createElement("p");
            const inside_a = document.createElement("a");
            const outside_a = document.createElement("a");

            section_2.appendChild(div);
            div.appendChild(img);
            div.appendChild(s_div);
            s_div.appendChild(link_div)
            link_div.appendChild(inside_a);
            link_div.appendChild(outside_a);
            s_div.appendChild(p);

            div.classList.add("following-section-2-contributorDiv");
            img.classList.add("sec_2_contributorImgfile");
            p.classList.add("following-section-2-contributorp");
            link_div.classList.add("following-section-2-contributor-linkDiv")
            inside_a.classList.add("following-section-2-contributor-inside-a");
            outside_a.classList.add("following-section-2-contributor-outside-a")

            div.setAttribute("id", `${results[i].id}`);
            img.setAttribute("src", `${results[i].profile_image}`);
            outside_a.setAttribute("href", `${results[i].link}`);
            outside_a.setAttribute("target", "_blank");
            outside_a.textContent = "Unsplash";
            inside_a.textContent = `${results[i].username}`;
            inside_a.setAttribute("href", `/public/${results[i].id}`)
        }
    }
    // fetch api
    fetchData(page){
        if(post_flag) {
            return;
        };
        const url = `${window.port}/api/user/following?page=${page}`
        post_flag = true
        fetch(url)
        .then( async ( response )=>{
            const data = await response.json()
            post_flag = false
            return data
        })
        .then(( result )=>{
            this.display_following(result.message)
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