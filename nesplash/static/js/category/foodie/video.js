const section_2 = document.querySelector(".foodie-section-2");
const a = document.getElementsByClassName("foodie-a")[1]

var page = 0;
let post_flag = false

class Foodie {
    // display function
    display_foodie(results){
        a.style.color = 'blue';
        for(var i=0;i<results.length;i++){
            const div = document.createElement("div");
            const a = document.createElement("a");
            const s_div = document.createElement("div");
            const s_img = document.createElement("img");
            const video = document.createElement("video");
            const source = document.createElement("source");

            section_2.appendChild(div);
            div.appendChild(s_div);
            s_div.appendChild(s_img);
            s_div.appendChild(a);
            div.appendChild(video);
            video.appendChild(source);
            
            div.classList.add("foodie-section-2-videoDiv");
            source.classList.add("foodie-section-2-img");
            s_img.classList.add("sec_2_imgfile");
            s_div.classList.add("sec_2_videoTopDiv");
            a.classList.add("foodie-section-2-video_a");
            video.classList.add("foodie-video");

            div.setAttribute("id", `${results[i].id}`);
            source.setAttribute("src", `${results[i].videourl}`);
            source.setAttribute("type", "video/mp4");
            s_img.setAttribute("src", `https://images.pexels.com/users/avatars/2659/pixabay-617.png?auto=compress&fit=crop&h=60&w=60`);
            a.setAttribute("href", `${results[i].link}`);
            a.setAttribute("target", "_blank");
            a.textContent = `${results[i].name}`;
            video.setAttribute("controls", "")
            video.setAttribute("muted", "");
        }
        
    }
    // fetch api
    fetchData(page){
        if(post_flag) {
            return;
        };
        const url = `${window.port}/foodie/api/videos?page=${page}`;
        post_flag = true;
        fetch(url)
        .then( async (response)=>{
            const data = await response.json()
            post_flag = false
            return data
        })
        .then((result)=>{
            this.display_foodie(result.message)
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
    const foodie = new Foodie
    foodie.fetchData(page)
})