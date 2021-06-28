const btn = document.querySelector(".signin-btn");

class Login {
    submitRequest(){
        btn.onclick = (e)=>{
            e.preventDefault()
            const url = `http://127.0.0.1:5000/api/user`
            fetch(url,{
                method: "PATCH",
                body: JSON.stringify({
                    email: document.querySelector(".signin-email").value,
                    password: document.querySelector(".signin-password").value
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
                    location.href = `${window.port}` + "/" 
                }
                else if(result.message == "none exist user"){
                    if(!document.querySelector('.signin-error')){
                        const error = document.createElement('p');
                        const errorsignin = btn.parentNode.insertBefore(error, btn);
                        errorsignin.textContent = 'none exist user';
                        errorsignin.classList.add('signin-error');
                    }
                    else if(document.querySelector('.signin-error').textContent === 'wrong password'){
                        document.querySelector('.signin-error').textContent = 'none exist user';
                    }
                }
                else if(result.message == "wrong password"){
                    if(!document.querySelector('.signin-error')){
                        const error = document.createElement('p');
                        const errorsignin = btn.parentNode.insertBefore(error, btn);
                        errorsignin.textContent = 'wrong password';
                        errorsignin.classList.add('signin-error');
                    }
                    else if(document.querySelector('.signin-error').textContent === "none exist user"){
                        document.querySelector('.signin-error').textContent = 'wrong password';
                    }
                }
            })
        }
    }
}

document.addEventListener("DOMContentLoaded", ()=>{
    const login = new Login
    login.submitRequest()
})