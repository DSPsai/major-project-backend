const selectImage = document.querySelector('.select-image');
const inputFile = document.querySelector('#file');
const imgArea = document.querySelector('.img-area');
selectImage.addEventListener('click', function () {
	inputFile.click();
})

inputFile.addEventListener('change', function (e) {
	const image = this.files[0]
	if(image.size < 2000000) {
		const reader = new FileReader();
		reader.onload = ()=> {
			const allImg = imgArea.querySelectorAll('img');
			allImg.forEach(item=> item.remove());
			const imgUrl = reader.result;
			const img = document.createElement('img');
			img.src = imgUrl;
			imgArea.appendChild(img);
			imgArea.classList.add('active');
			imgArea.dataset.img = image.name;
		}
		reader.readAsDataURL(image);
		let formdata=new FormData()
		formdata.append('file',e.target.files[0])
		axios.post('http://localhost:8000',formdata).then(res=>{console.log(res)}).catch(er=>console.log(er))
	} else {
		alert("Image size more than 2MB");
	}
})