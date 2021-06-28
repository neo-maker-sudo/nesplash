const btn = document.querySelector(".resetRequest-btn");
const input = document.querySelector(".resetRequest-email");


class Reset {
    reset_password(){
        btn.onclick = ()=>{
            const url = `${window.port}/api/user/reset-page`
            fetch(url,{
                method: "POST",
                body: JSON.stringify({
                    email: input.value
                }),
                headers: {
                    "Content-Type": "application/json"
                }
            })
            .then( async (response)=>{
                return await response.json()
            })
            .then((result)=>{
                if(result.ok == true){
                    location.href = `${window.port}` + "/"
                }
                if(result.error == "none exist user"){
                    alert("查無此使用者")
                }
            })
        }
    }
}

document.addEventListener("DOMContentLoaded", ()=>{
    const reset = new Reset
    reset.reset_password()
})