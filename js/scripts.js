/*!
 * Start Bootstrap - Shop Homepage v5.0.6 (https://startbootstrap.com/template/shop-homepage)
 * Copyright 2013-2023 Start Bootstrap
 * Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-shop-homepage/blob/master/LICENSE)
 */
// This file is intentionally blank
// Use this file to add JavaScript to your project

/*篩選邏輯*/
function filterBikes() {
    const keyword = document.getElementById('search').value.toLowerCase();
    const brand = document.getElementById('brand-select').value;
    const maxPrice = parseInt(document.getElementById('price-select').value);
    const mileageRange = document.getElementById('mileage-select').value;
    const store = document.getElementById('store-select').value;

    const bikes = document.querySelectorAll('.bike-card');

    bikes.forEach(bike => {
        const card = bike.querySelector('.card');

        const name = card.dataset.name.toLowerCase();
        const bikeBrand = card.dataset.brand;
        const price = parseInt(card.dataset.price);
        const mileage = parseInt(card.dataset.mileage); // 里程（km）
        const bikeStore = card.dataset.store;

        // 篩選條件
        const matchesKeyword = name.includes(keyword);
        const matchesBrand = (brand === '' || brand === bikeBrand);
        const matchesPrice = (isNaN(maxPrice) || price <= maxPrice);
        const matchesStore = (store === '' || store === bikeStore);
        const matchesMileage = checkMileage(mileage, mileageRange);

        // 綜合判斷是否顯示
        if (matchesKeyword && matchesBrand && matchesPrice && matchesMileage && matchesStore) {
            bike.style.display = 'block';
        } else {
            bike.style.display = 'none';
        }
    });
}

// 里程條件檢查（分段範圍）
function checkMileage(mileage, range) {
    switch (range) {
        case '1': // 0 - 5000 km
            return mileage <= 5000;
        case '2': // 5001 - 30000 km
            return mileage > 5000 && mileage <= 30000;
        case '3': // 30001 - 50000 km
            return mileage > 30000 && mileage <= 50000;
        case '4': // > 50000 km
            return mileage > 50000;
        default: // 未選擇任何範圍
            return true;
    }
}