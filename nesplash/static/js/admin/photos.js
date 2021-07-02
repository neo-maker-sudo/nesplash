const a = document.getElementsByClassName("admin-a")[1];
const searchBtn = document.getElementById("search-button");
const section_2 = document.querySelector(".admin-section-2");

const mainSwitch_1 = document.getElementsByClassName("close")[0];
const model_delete = document.getElementById("modal-delete");
const confirmDelete = document.querySelector(".delete-button");

let id ;
var post_flag = false;

class Admin {
    // admin delete user photo api
    deletePhoto(){
        confirmDelete.onclick = ()=>{
            const url = `${window.port}/api/admin/delete/photos-data`;
            fetch(url,{
                method: 'DELETE',
                body: JSON.stringify({
                    photo_id: id
                }),
                headers: {
                    "Content-Type": "application/json"
                }
            })
            .then( async ( response )=>{
                return await response.json()
            })
            .then(( result )=>{
                if(result.ok == true){
                    window.location.reload()
                }
                else{
                    alert("照片不存在，請排除問題")
                }
            })
        }
    }
    // modal close function
    close(){
        mainSwitch_1.onclick = ()=>{
            model_delete.style.display = "none";
        }   
    }
    // modal confirm page function
    showConfirmPage(){
        const deleteBtn = document.querySelector(".photos-button");
        deleteBtn.onclick = ()=>{
            const photo = document.querySelector(".photos-img");
            model_delete.style.display = "block";
            id = photo.id;
            this.deletePhoto()
        }
    }
    // remove pervious photos let new photo replace function
    removeAttraction(){
        while(section_2.hasChildNodes()){
            section_2.removeChild(section_2.firstChild)
        }
    }
    // display user's photo after search api function
    async display_data(result){
        await this.removeAttraction()

        const div = document.createElement("div");
        const a = document.createElement("a");
        const img = document.createElement("img");
        const button = document.createElement("button");

        section_2.appendChild(div);
        div.appendChild(a);
        div.appendChild(img);
        div.appendChild(button);

        div.classList.add("photos-div");
        a.textContent = `${result.username}`;
        a.classList.add("photos-a");
        a.setAttribute("href", `/public/${result.user_id}`);
        a.setAttribute("target", "_blank");
        img.classList.add("photos-img");

        if(result.imageurl.split(".")[1] == "jpg"){
            img.setAttribute("src", `/static/public_pics/${result.imageurl}`);
        }
        else if(result.imageurl.split(".")[1] == "png"){
            img.setAttribute("src", `/static/public_pics/${result.imageurl}`);
        }
        else{  
            img.setAttribute("src", `${result.imageurl}`);
        }
        img.setAttribute("id", `${result.id}`)
        button.textContent = "Delete";
        button.classList.add("photos-button");
        
        this.showConfirmPage()
    }
    // search user's photo api
    searchData(){
        a.style.color = "blue";
        searchBtn.onclick = ()=>{
            if(post_flag) {
                return;
            };
            const photo_input = document.querySelector(".search-input")

            post_flag = true
            const url = `${window.port}/api/admin/photos-data`
            fetch(url,{
                method: 'POST',
                body: JSON.stringify({
                    photo_id: photo_input.value
                }),
                headers: {
                    "Content-Type": "application/json"
                }
            })
            .then( async ( response )=>{
                const data = await response.json()
                post_flag = false
                return data
            })
            .then((result)=>{
                if(result.error == "none exist photo"){
                    alert("照片不存在，請排除問題");
                    return;
                }
                this.display_data(result.message)
            })
        }
    }
}


document.addEventListener("DOMContentLoaded", ()=>{
    const admin = new Admin
    admin.searchData()
    admin.close()
})
