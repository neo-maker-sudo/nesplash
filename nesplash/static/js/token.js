const btn = document.querySelector(".resetRequest-btn");
const input = document.querySelector(".resetRequest-password");
const confirm_input = document.querySelector(".resetRequest-confirm-password");


class Password {
    tokenDeliver(){
        btn.onclick = ()=>{
            if(confirm_input.value !== input.value){
                alert("密碼與確認密碼不符")
            }
            const token = location.pathname.split("/")[4]
            const url = `${window.port}/api/user/reset-password/${token}`
            fetch(url,{
                method: "POST",
                body: JSON.stringify({
                    password: input.value,
                    conform_password: confirm_input.value
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
                    location.href = `${window.port}` + "/signin"
                }
                else if(result.error == "password and conform_password not same"){
                    alert("密碼與確認密碼不符")
                }
                else if(result.error == "Invalid or expired token"){
                    alert("申請效期過期，請重新申請忘記密碼")
                }
            })
        }

    }
}

document.addEventListener("DOMContentLoaded", ()=>{
    const password = new Password
    password.tokenDeliver()
})