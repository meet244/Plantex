let predictionImg = document.getElementById('prediction-image');
let predictionName = document.getElementById('prediction-name');
let predictionDesc = document.getElementById('prediction-desc');
window.addEventListener('DOMContentLoaded', () => {
	const url = new URL(window.location.href);
	const params = new URLSearchParams(url.search);
	const disease = params.get('disease');
	let formData = new FormData();
	formData.append('disease', disease);
	return fetch('http://192.168.12.104:5001/diseasedetail', {
		method: 'POST',
		body: formData,
	})
		.then((response) => response.json())
		.then((result) => {
			let { link, name, description } = result;
			predictionImg.style.backgroundImage = `url(${link})`;
			predictionName.innerHTML = name;
            predictionDesc.innerHTML = description.map((desc) => `<li>${desc}</li>`).join('');
		});
});
