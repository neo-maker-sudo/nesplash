const title = document.querySelector(".confirm-title");
const cname = document.querySelector(".confirm-name");

class Confirm {
    // if success response function
    success(message){
        cname.textContent = `Hello, ${message} `
        title.textContent = `Account Confirm success`
    }
    // if fail response function
    error(message){
        title.textContent = `${message}, Please contact offical stall eyywqkgb@gmail.com`
    }
    // fetch api
    fetchData(){
        const token = location.pathname.split("/")[4]
        const url = `${window.port}/api/user/confirm-email`
        fetch(url,{
            method : "POST",
            body : JSON.stringify({
                token: token
            }),
            headers : {
                "Content-Type": "application/json"
            }
        })
        .then( async ( response )=>{
            return await response.json()
        })
        .then(( result )=>{
            if(result.ok == true){
                this.success(result.message)
            }
            else {
                this.error(result.message)
            }
        })
    }
}

document.addEventListener("DOMContentLoaded", ()=>{
    const confirm = new Confirm
    confirm.fetchData()
})