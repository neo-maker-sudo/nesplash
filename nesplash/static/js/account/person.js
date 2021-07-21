const li = document.getElementsByClassName("account-2-a")[0];

const mainSwitch_1 = document.getElementsByClassName("close")[0];
const mainSwitch_2 = document.getElementsByClassName("close")[1];
const mainSwitch_3 = document.getElementsByClassName("close")[2];
const mainSwitch_4 = document.getElementsByClassName("close")[3];
const mainSwitch_5 = document.getElementsByClassName("close")[4];
const mainSwitch_6 = document.getElementsByClassName("close")[5];

const model_name = document.getElementById("modal-name");
const model_change_password = document.getElementById("modal-change-password");
const model_location = document.getElementById("modal-location");
const model_link = document.getElementById("modal-link");
const model_delete = document.getElementById("modal-delete");
const model_upload = document.getElementById("modal-upload");

const idDiv = document.querySelector(".person-topDiv");
const public_page = document.querySelector(".person-public");
const spanDiv = document.querySelector(".person-confirm-spanDiv");

const modify_1 = document.querySelector(".person-modify-1");
const modify_2 = document.querySelector(".person-modify-2");
const modify_3 = document.querySelector(".person-modify-3");
const modify_4 = document.querySelector(".person-modify-4");
const modify_5 = document.querySelector(".person-modify-5");
const delete_account = document.querySelector(".person-delete");

const name_btn = document.querySelector(".name-button");
const change_password_btn = document.querySelector(".change-password-button");
const delete_btn = document.querySelector(".delete-button")
const location_btn = document.querySelector(".location-button");
const link_btn = document.querySelector(".link-button");
const image_profile_btn = document.querySelector(".upload-btn");
const public_image_btn = document.querySelector(".upload-button");

const change_location_input = document.getElementById("location-input");
const change_link_input = document.getElementById("link-input");
const change_username_input_1 = document.getElementById("name-input_1");
const chage_password_input_1 = document.getElementById("change-password-input_1");
const chage_password_input_2 = document.getElementById("change-password-input_2");

const iform = document.getElementById("iform");
const iform_2 = document.getElementById("iform_2");
const upload_publicImg = document.querySelector(".person-upload");
const upload_div = document.querySelector(".upload-div");

const categoryLi = document.getElementsByClassName("category-li");
const categoryTextarea = document.querySelector(".upload-textarea");


let index = 0;
let category_status ;
let method;

class Person {
    // display select category function
    liColor(){
        for(var i=0;i<categoryLi.length;i++){
            categoryLi[i].style.background = '';
        }
        categoryLi[index].style.background = '#36a162'
    }
    // upload public image api
    upload_publicImage(){
        upload_publicImg.onclick = ()=>{
            model_upload.style.display = "block";
            for(let i=0;i<categoryLi.length;i++){
                categoryLi[i].num = i
                categoryLi[i].onclick = ()=>{
                    index = categoryLi[i].num;
                    category_status = categoryLi[i].textContent
                    this.liColor()
                }
            }
            public_image_btn.onclick = (e)=>{ 
                e.preventDefault()
                if(iform_2.files[0] == undefined){
                    alert("請選擇圖片檔案");
                    return;
                }
                else if(category_status == undefined){
                    alert("請選擇一個Category類別");
                    return
                }
                else{
                    const size = iform_2.files[0]["size"] / 1024 / 1024
                    const type = iform_2.files[0]["type"].split("/")[1]
                    if (size > 10) {
                        alert("傳輸檔案請小於10MB")
                        return
                    }

                    if( type === "jpeg" || type === "png"){
                        public_image_btn.classList.add("loading-div");
                        public_image_btn.textContent = "submitting";

                        const url = `${window.port}/api/user/upload-public-image`

                        var formData = new FormData()
                        formData.append("file", iform_2.files[0]);
                        formData.append("description", categoryTextarea.value);
                        formData.append("category", category_status);

                        fetch(url, {
                            method: "POST",
                            body : formData
                        })
                        .then( async (response)=>{
                            return await response.json()
                        })
                        .then((result)=>{
                            if(result.ok == true){
                                location.href = `${window.port}` + "/account/upload_pictures"
                            }
                            if(result.message == "you are not allow to do this action"){
                                location.href = `${window.port}` + "/"
                            }
                        })
                    } else {
                        alert("錯誤照片格式")
                        return
                    }
                }
            }
        }
    }
    // upload profile image api
    upload_bigImage(){
        image_profile_btn.onclick = (e)=>{
            e.preventDefault()
            if(iform.files[0] == undefined){
                alert("請選擇圖片檔案");
                return;
            }else{
                const size = iform.files[0]["size"] / 1024 / 1024 // Mib
                const type = iform.files[0]["type"].split("/")[1]
                if(size > 2){
                    alert("傳輸檔案請小於2MB")
                    return;
                }
                if( type === "jpeg" || type === "png"){
                    const url = `${window.port}/api/user/upload-profile-image`
                    var formData = new FormData()

                    formData.append("file", iform.files[0])

                    fetch(url, {
                        method: "POST",
                        body : formData
                    })
                    .then( async (response)=>{
                        return await response.json()
                    })
                    .then((result)=>{
                        if(result.ok == true){
                            window.location.reload()
                        }
                        if(result.message == "you are not allow to do this action"){
                            location.href = `${window.port}` + "/"
                        }
                    })
                } else {
                    alert("錯誤照片格式")
                    return
                }
            }
        }
    }
    // delete account api
    delete_account(){
        delete_account.onclick = ()=>{
            model_delete.style.display = "block";
            delete_btn.onclick = ()=>{
                const url = `${window.port}/api/user/delete-account`
                fetch(url, {
                    method: "DELETE"
                })
                .then( async (response) => {
                    return await response.json()
                })
                .then((result)=>{
                    if(result.ok == true){
                        location.href = `${window.port}` + "/" 
                    }
                })
            }
        }
    }
    // change personal data api
    modify(){
        modify_1.onclick = ()=>{
            model_name.style.display = "block";
            name_btn.onclick = ()=>{
                if(change_username_input_1.value == ""){
                    alert("無法送出空值")
                    return
                }
                const url = `${window.port}/api/user/change-username`;
                fetch(url,{
                    method: "POST",
                    body : JSON.stringify({
                        "username": change_username_input_1.value
                    }),
                    headers : {
                        "Content-Type": "application/json"
                    }
                })
                .then( async (response)=>{
                    return await response.json()
                })
                .then((result)=>{
                    if(result.ok == true){
                        window.location.reload();
                    }
                    else if (result.error == "none exist user"){
                        alert("none exist user");
                    }
                    else if (result.error == "username already be taken, change anthor one"){
                        alert("username already be taken, change anthor one");
                    }
                })
            }
            
        }
        modify_2.onclick = ()=>{
            model_change_password.style.display = "block";
            change_password_btn.onclick = ()=>{
                if(method == "google"){
                    alert("your account is google, don't need to change passowrd")
                }
                else if(method == "github"){
                    alert("your account is github, don't need to change password")
                }
                else{
                    const url = `${window.port}/api/user/change-password`
                    fetch(url,{
                        method: "POST",
                        body : JSON.stringify({
                            "password": chage_password_input_1.value,
                            "conform_password": chage_password_input_2.value
                        }),
                        headers : {
                            "Content-Type": "application/json"
                        }
                    })
                    .then( async (response)=>{
                        return await response.json()
                    })
                    .then((result)=>{
                        if(result.ok == true){
                            alert("Password change success");
                            model_change_password.style.display = "none";
                            chage_password_input_1.value = "";
                            chage_password_input_2.value = "";
                        }
                        else if (result.error == "none exist user"){
                            alert("none exist user");
                        }
                    })
                }
            }
        }
        modify_3.onclick = ()=>{
            const textarea = document.querySelector(".textarea-bio");
            const url = `${window.port}/api/user/change-bio`
            fetch(url,{
                method: "POST",
                body : JSON.stringify({
                    "bio": textarea.value
                }),
                headers : {
                    "Content-Type": "application/json"
                }
            })
            .then( async (response)=>{
                return await response.json()
            })
            .then((result)=>{
                if(result.ok == true){
                    window.location.reload();
                }
            })
        }
        modify_4.onclick = ()=>{
            model_location.style.display = "block";
            location_btn.onclick = ()=>{
                const url = `${window.port}/api/user/change-location`;
                fetch(url,{
                    method: "POST",
                    body : JSON.stringify({
                        "location": change_location_input.value
                    }),
                    headers : {
                        "Content-Type": "application/json"
                    }
                })
                .then( async (response)=>{
                    return await response.json()
                })
                .then((result)=>{
                    if(result.ok == true){
                        window.location.reload();
                    }
                    else if (result.error == "none exist user"){
                        alert("none exist user");
                    }
                })
            }
        }
        modify_5.onclick = ()=>{
            model_link.style.display = "block";
            link_btn.onclick = ()=>{
                const url = `${window.port}/api/user/change-link`;
                fetch(url,{
                    method: "POST",
                    body : JSON.stringify({
                        "link": change_link_input.value
                    }),
                    headers : {
                        "Content-Type": "application/json"
                    }
                })
                .then( async (response)=>{
                    return await response.json()
                })
                .then((result)=>{
                    if(result.ok == true){
                        window.location.reload();
                    }
                    else if (result.error == "none exist user"){
                        alert("none exist user");
                    }
                })
            }
        }
    }
    // modal close function
    close(){
        mainSwitch_1.onclick = ()=>{
            model_name.style.display = "none";
        }
        mainSwitch_2.onclick = ()=>{
            model_change_password.style.display = "none";
        }
        mainSwitch_3.onclick = ()=>{
            model_location.style.display = "none";
        }
        mainSwitch_4.onclick = ()=>{
            model_link.style.display = "none";
        }
        mainSwitch_5.onclick = ()=>{
            model_delete.style.display = "none";
        }
        mainSwitch_6.onclick = ()=>{
            model_upload.style.display = "none";
            public_image_btn.classList.remove("loading-div");
        }
    }
    // display personal data function
    display_personTopDiv(data){
        console.log(data)
        li.classList.add("select");

        const name = document.querySelector(".label-name");
        const email = document.querySelector(".label-email");
        const location = document.querySelector(".label-location");
        const link = document.querySelector(".label-link")
        const bio = document.querySelector(".textarea-bio");
        const pro_fileImage = document.querySelector(".person-image");
        const status = document.querySelector(".confirm-status");
        

        idDiv.setAttribute("id", `${data.id}`);
        method = data.Method.user_method
        if(data.Method.user_method == "google"){
            const google = document.querySelector(".bind-googleDiv");
            const google_span = document.createElement("span");
            google.appendChild(google_span);
            google_span.textContent = `----- ${data.username}`
            
        }
        else if(data.Method.user_method == "github"){
            const github = document.querySelector(".bind-githubDiv");
            const github_span = document.createElement("span");
            github.appendChild(github_span);
            github_span.textContent = `----- ${data.username}`;
        }
        else{
            const neo = document.querySelector(".bind-neoDiv");
            const neo_span = document.createElement("span");
            neo.appendChild(neo_span);
            neo_span.textContent = `----- ${data.username}`;
        }

        pro_fileImage.setAttribute("src", `${data.profile_image}`)
        name.textContent = `${data.username}` == "" ? "anonymous" : `${data.username}`;
        email.textContent = `${data.email}`;
        
        if (data.location !== null){
            if (data.location === ""){
                location.textContent = `${data.location}`
            } else {
                location.textContent = `${data.location}`
            }
        }
        
        if (data.link !== null){
            if (data.link === ""){
                link.textContent = `${data.link}`
            }else{
                if(data.link.split(".")[0] === "www"){
                    link.textContent = `${data.link}`;
                    link.setAttribute("href", `https://${data.link}`);
                }else{
                    link.textContent = `${data.link}`;
                    link.setAttribute("href", `${data.link}`);
                }
                link.setAttribute("target", "_blank")
            }
        }
        if (data.bio !== null){
            if (data.bio === ""){
                bio.textContent = `${data.bio}`;
            } else {
                bio.textContent = `${data.bio}`;
            }
        }
        
        public_page.setAttribute("href", `/public/${data.id}`);
        public_page.setAttribute("target", `_blank`);
        if(data.lock_status == true){
            spanDiv.classList.add("success");
            status.textContent = "Account Confrimed";
            upload_publicImg.className = "person-upload-forbidden";
            const remind_span = document.createElement("span")
            idDiv.appendChild(remind_span);
            remind_span.textContent = "Your account already been lock, can not upload images, if you have issue please contact administrator email: eyywqkgb@gmail.com";
            remind_span.classList.add("remind-span");
            return;
        }

        if(data.confirmed_status == true){
            status.textContent = "Account Confrimed";
            spanDiv.classList.add("success");
            this.upload_publicImage()
        }
        else{
            status.textContent = "Account UnConfrim";
            upload_publicImg.className = "person-upload-forbidden";
            const remind_span = document.createElement("span")
            idDiv.appendChild(remind_span);
            remind_span.textContent = "Your account not confirm yet, if you have issue please contact administrator email: eyywqkgb@gmail.com";
            remind_span.classList.add("remind-span");
        }
        
    }
    // fetch api
    fetchData(){
        const url = `${window.port}/api/account/data`
        fetch(url)
        .then( async ( response )=>{
            return await response.json()
        })
        .then(( result )=>{
            this.display_personTopDiv(result.message)
        })
    }
}


document.addEventListener("DOMContentLoaded", ()=>{
    const person = new Person
    person.fetchData()
    person.upload_bigImage()
    person.modify()
    person.delete_account()
    person.close()
})