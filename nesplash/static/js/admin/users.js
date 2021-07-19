const admin_section_2 = document.querySelector(".admin-section-2");
const model_password = document.getElementById("modal-password");
const model_authority = document.getElementById("modal-authority");

const mainSwitch_1 = document.getElementsByClassName("close")[0];
const mainSwitch_2 = document.getElementsByClassName("close")[1];
const password_btn = document.querySelector(".password-button");
const authority_btn = document.querySelector(".authority-button");
const searchBtn = document.getElementById("search-button");

const authorityLi = document.getElementsByClassName("authority-li");
const a = document.getElementsByClassName("admin-a")[0];

let id;
let index = 0;
let authority_status;
var post_flag = false;

class Admin {
    // admin send change password api
    resend(){
        password_btn.onclick = ()=>{
            const url = `${window.port}/api/admin/help-resend-mail`
            fetch(url, {
                method: "POST",
                body: JSON.stringify({
                    id: id
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
                    alert("發送成功");
                    model_password.style.display = "none";
                }
                else{
                    alert("使用者不存在，請排除異常")
                }
            })
        }
    }
    // modal close function
    close(){
        mainSwitch_1.onclick = ()=>{
            model_password.style.display = "none";
        }   
        mainSwitch_2.onclick = ()=>{
            model_authority.style.display = "none";
        }
    }
    // forget password confirm page function
    send_forget_mail(){
        const forgetBtn = document.getElementsByClassName("admin-forgetBtn");
        for(let i=0;i<forgetBtn.length;i++){
            forgetBtn[i].onclick = ()=>{
                model_password.style.display = "block";
                id = forgetBtn[i].id
            }
        }
        this.resend()
    }

    // lock or unlock user's authority api
    authorize(){
        authority_btn.onclick = ()=>{
            if(authority_status == "Lock"){
                const url = `${window.port}/api/admin/lock-authority`;
                fetch(url, {
                    method: "POST",
                    body: JSON.stringify({
                        id: id
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
                        alert("發送成功");
                        model_authority.style.display = "none";
                    }
                    else{
                        alert("使用者不存在，請排除異常")
                    }
                })
            }else if(authority_status == "Unlock"){
                const url = `${window.port}/api/admin/unlock-authority`;
                fetch(url, {
                    method: "POST",
                    body: JSON.stringify({
                        id: id
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
                        alert("發送成功");
                        model_authority.style.display = "none";
                    }
                    else{
                        alert("使用者不存在，請排除異常")
                    }
                })
            }
        }
    }

    // lock or unlock user's authority confirm page function
    lock_authority(){
        const lockBtn = document.getElementsByClassName("admin-lockBtn");
        for(let i=0;i<lockBtn.length;i++){
            lockBtn[i].onclick = ()=>{
                model_authority.style.display = "block";
                id = lockBtn[i].id
                for(let i=0;i<authorityLi.length;i++){
                    authorityLi[i].num = i
                    authorityLi[i].onclick = ()=>{
                        index = authorityLi[i].num;
                        authority_status = authorityLi[i].textContent
                        this.liColor()
                    }
                }
            }
        }
        this.authorize()
    }

    // display select lock or unlock function
    liColor(){
        for(var i=0;i<authorityLi.length;i++){
            authorityLi[i].style.background = '';
        }
        authorityLi[index].style.background = '#36a162'
    }

    // display all user function
    display_users(data){
        for(let i=1;i<data.length;i++){
            const userDiv = document.createElement("div");
            const userImage = document.createElement("img");
            const gridDiv = document.createElement("div");
            const userName = document.createElement("a");
            const div = document.createElement("div");
            const forgetBtn = document.createElement("button");
            const lockBtn = document.createElement("button");
            
            admin_section_2.appendChild(userDiv)
            userDiv.appendChild(userImage);
            userDiv.appendChild(gridDiv);
            gridDiv.appendChild(userName);
            gridDiv.appendChild(div);
            div.appendChild(forgetBtn);
            div.appendChild(lockBtn);
            userDiv.classList.add("admin-userDiv");
            userImage.classList.add("admin-userImage");

            userImage.setAttribute("src", `${data[i].profile_image}`);
            gridDiv.classList.add("admin-gridDiv");
            userName.textContent = `${data[i].username}`;
            userName.classList.add("admin-userName");
            userName.setAttribute("href", `/public/${data[i].id}`);
            userName.setAttribute("target", `_blank`);
            forgetBtn.textContent = "password";
            forgetBtn.classList.add("admin-forgetBtn");
            forgetBtn.setAttribute("id", `${data[i].id}`);
            lockBtn.textContent = "authority";
            lockBtn.classList.add("admin-lockBtn");
            lockBtn.setAttribute("id", `${data[i].id}`);
        }
        this.send_forget_mail()
        this.lock_authority()
    }

    // display search users
    async search_users(data){
        await this.removeUsers()

        for(let i=0;i<data.length;i++){
            const userDiv = document.createElement("div");
            const userImage = document.createElement("img");
            const gridDiv = document.createElement("div");
            const userName = document.createElement("a");
            const div = document.createElement("div");
            const forgetBtn = document.createElement("button");
            const lockBtn = document.createElement("button");
            
            admin_section_2.appendChild(userDiv)
            userDiv.appendChild(userImage);
            userDiv.appendChild(gridDiv);
            gridDiv.appendChild(userName);
            gridDiv.appendChild(div);
            div.appendChild(forgetBtn);
            div.appendChild(lockBtn);
            userDiv.classList.add("admin-userDiv");
            userImage.classList.add("admin-userImage");

            userImage.setAttribute("src", `${data[i].profile_image}`);
            gridDiv.classList.add("admin-gridDiv");
            userName.textContent = `${data[i].username}`;
            console.log(data[i].username)
            userName.classList.add("admin-userName");
            userName.setAttribute("href", `/public/${data[i].id}`);
            userName.setAttribute("target", `_blank`);
            forgetBtn.textContent = "password";
            forgetBtn.classList.add("admin-forgetBtn");
            forgetBtn.setAttribute("id", `${data[i].id}`);
            lockBtn.textContent = "authority";
            lockBtn.classList.add("admin-lockBtn");
            lockBtn.setAttribute("id", `${data[i].id}`);
        }
        this.send_forget_mail()
        this.lock_authority()
    }

    // remove exist users
    removeUsers(){
        while(admin_section_2.hasChildNodes()){
            admin_section_2.removeChild(admin_section_2.firstChild)
        }
    }
    // search api
    searchData(){
        searchBtn.onclick = (e)=>{
            e.preventDefault()
            const user_input = document.querySelector(".search-input")
            if(post_flag){
                return
            }

            post_flag = true
            const url = `${window.port}/api/admin/users-data`
            fetch(url,{
                method: 'POST',
                body: JSON.stringify({
                    "username": user_input.value
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
                if(result.ok == true){
                    this.search_users(result.message)
                }
            })
        }
    }
    // fetch api
    fetchData(){
        a.style.color = "blue"
        const url = `${window.port}/admin/users`;
        fetch(url)
        .then( async ( response )=>{
            return await response.json()
        })
        .then((result)=>{
            if(result.ok == true){
                this.display_users(result.message)
            }
        })
    }
}

document.addEventListener("DOMContentLoaded", ()=>{
    const admin = new Admin
    admin.fetchData()
    admin.searchData()
    admin.close()
})