const homeproducts = document.getElementById("id-product_container");

let showproducts = [
  { title: "Cacti Plant", price: 10.23, imgUrl: "img/product1.png" },
  { title: "Cacti Plant", price: 20.23, imgUrl: "img/product2.png" },
  { title: "Cacti Plant", price: 40.21, imgUrl: "img/product3.png" },
  { title: "Cacti Plant", price: 10.23, imgUrl: "img/product4.png" },
  { title: "Cacti Plant", price: 13.23, imgUrl: "img/product5.png" },
  { title: "Cacti Plant", price: 13.23, imgUrl: "img/product5.png" },
  { title: "Cacti Plant", price: 10.23, imgUrl: "img/product6.png" },
  { title: "Cacti Plant", price: 10.23, imgUrl: "img/product6.png" },
];

function productsHtml(products) {
  let code = products
    .map((product) => {
      return `
    <article class="product__card">
    <div class="product__circle"></div>
    
    <img src=${product.imgUrl} alt="" class="product__img">

    <h3 class="product__title">${product.title}</h3>
    <span class="product__price">$${product.price}</span>

    <button class="button--flex product__button">
    <i class="ri-shopping-bag-line"></i>
    </button>
    </article>
    `;
    })
    .join("");
  homeproducts.innerHTML = code;
}
window.addEventListener("DOMContentLoaded", productsHtml(showproducts));
