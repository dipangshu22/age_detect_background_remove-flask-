function uploadImage(){

let fileInput = document.getElementById("fileInput")

let formData = new FormData()
formData.append("image", fileInput.files[0])

fetch("/predict",{
method:"POST",
body:formData
})
.then(res=>res.json())
.then(data=>{

if(data.error){
document.getElementById("result").innerHTML=data.error
return
}

document.getElementById("result").innerHTML=
`
<img src="${data.image}" width="250">
<h2>Predicted Age: ${data.age}</h2>
`
})
}