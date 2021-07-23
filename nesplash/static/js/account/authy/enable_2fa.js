const enableBtn = document.getElementById("enable-2fa-button");

class Enable {
    send() {
        enableBtn.onclick = ()=>{
            const url =`${window.port}/api/user/2fa/enable`
            fetch(url, {
                method: "POST"
            })
            .then( async ( response )=>{
                return await response.json()
            })
            .then((result)=>{
                if(result.ok == true){
                    window.location = `${window.port}` + "/2fa/qrcode/enable"
                } else {
                    alert("異常，請聯繫管理人員，eyywqkgb@gmail.com")
                }
            })
        }
    }
}



document.addEventListener("DOMContentLoaded", ()=>{
    const enable = new Enable
    enable.send()
})