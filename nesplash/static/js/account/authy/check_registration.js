let count = 0;

function check_registration() {
    const url = `${window.port}/api/user/2fa/enable/poll`
    fetch(url)
    .then( async (response)=>{
        return await response.json()
    })
    .then(( result )=>{
        if(result.message == "pending") {
            if(count === 60){
                alert("QRCODE超過時效，請回會員頁面重新操作")
                clearTimeout(myVar)
                return
            }
            count += 1;
            clearTimeout(myVar)
            myVar = setTimeout(check_registration, 5000);
        } else if (result.message == "completed") {
            window.location = `${window.port}` + "/account/data"
        } else {
            alert("異常，請聯繫管理人員 : eyywqkgb@gmail.com")
        }
    })
}

myVar = setTimeout(check_registration, 5000);