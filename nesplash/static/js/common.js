const signin = document.getElementById("signin");
const signup = document.getElementById("signup");
const nav_right = document.querySelector(".nav-li-right");


class Common {
    // change navbar info
    statusChange(data){
        // signin
        if(data.role_id == "3"){
            const a = document.createElement("a");
            const admin = signin.parentNode.insertBefore(a,signin)
            admin.classList.add("navbar-brand-2");
            admin.setAttribute("href", "/admin")
            admin.textContent = "Admin"
        }
        signin.setAttribute("id", "account");
        signin.setAttribute("href", "/account/data");
        signin.textContent = `${data.username}`;
        // signup
        signup.removeAttribute("href");
        signup.setAttribute("id", "logout");
        signup.textContent = "logout";
    }

    // check status
    confirmIdentity(){
        const url = `${window.port}/api/user`
        fetch(url)
        .then( async ( response )=>{
            return await response.json()
        })
        .then((result)=>{
            
            if(result.message != null){
                this.statusChange(result.message)
                
                const logout = document.getElementById("logout");
                logout.onclick = ()=>{
                    const url = `${window.port}/api/user`
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
            else{
                // signin 
                signin.setAttribute("id", "signin");
                signin.setAttribute("href", "/signin");
                signin.textContent = "Signin";
                // signup
                signin.setAttribute("id", "signup");
                signup.setAttribute("href", "/signup");
                signup.textContent = "Signup";
            }
        })
    }
}

document.addEventListener("DOMContentLoaded", async ()=>{
    const common = new Common
    await common.confirmIdentity()

})