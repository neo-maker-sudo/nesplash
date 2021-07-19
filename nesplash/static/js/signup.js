const btn = document.querySelector(".signup-btn");

class Register {
    submitRequest(){
        btn.onclick = (e)=>{
            e.preventDefault()
            const url = `${window.port}/api/user`
            fetch(url, {
                method: "POST",
                headers : {
                    'Content-Type': 'application/json'
                },
                body : JSON.stringify({
                    email: document.querySelector(".signup-email").value,
                    username : document.querySelector(".signup-username").value,
                    password : document.querySelector(".signup-password").value
                })
            })
            .then( async (response)=>{
                return await response.json()
            })
            .then((result)=>{
                if(result.ok == true){
                    location.href = location.origin + "/signin"
                }   
                else if(result.message == "email has already been taken, please use another one"){
                    if(!document.querySelector('.signup-error')){
                        const error = document.createElement('p');
                        const errorSignup = btn.parentNode.insertBefore(error, btn);
                        errorSignup.textContent = 'email has already been taken, please use another one';
                        errorSignup.classList.add('signup-error');
                    }
                    else if(document.querySelector('.signup-error').textContent === 'duplicate username'){
                        document.querySelector('.signup-error').textContent = 'email has already been taken, please use another one';
                    }
                }
                else if(result.message == "duplicate username"){
                    if(!document.querySelector('.signup-error')){
                        const error = document.createElement('p');
                        const errorSignup = btn.parentNode.insertBefore(error, btn);
                        errorSignup.textContent = 'duplicate username';
                        errorSignup.classList.add('signup-error');
                    }
                    else if(document.querySelector('.signup-error').textContent === "email has already been taken, please use another one"){
                        document.querySelector('.signup-error').textContent = 'duplicate username';
                    }
                }
            })
        }
    }
}


document.addEventListener("DOMContentLoaded", ()=>{
    const register = new Register
    register.submitRequest()
})