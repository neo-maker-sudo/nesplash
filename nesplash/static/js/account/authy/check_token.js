const checkBtn = document.getElementById("twofa-check-button");
const checkinput = document.getElementById("twofa-check-input");


class Enable {
    send() {
        checkBtn.onclick = ()=>{
            if(checkinput.value.length === 7){
                const url =`${window.port}/api/user/2fa/check/token`
                fetch(url, {
                    method: "POST",
                    body: JSON.stringify({
                        "token": checkinput.value
                    }),
                    headers : {
                        "Content-Type": "application/json"
                    }
                })
                .then( async ( response )=>{
                    return await response.json()
                })
                .then((result)=>{
                    if(result.ok == true){
                        window.location = `${window.port}/account/data`
                    } else {
                        alert("授權碼錯誤")
                    }
                })
            } else {
                alert("請輸入7位數字授權碼")
            }
        }
    }
}






document.addEventListener("DOMContentLoaded", ()=>{
    const enable = new Enable
    enable.send()
})