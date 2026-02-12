function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}

function checkAuthentication() {
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');
    
    if (!token) {
        if (loginLink) loginLink.style.display = 'block';
        // اختياري: إذا أردت إظهار الأماكن حتى بدون تسجيل دخول (حسب متطلبات مشروعك)
        fetchPlaces(null); 
    } else {
        if (loginLink) loginLink.style.display = 'none';
        fetchPlaces(token);
    }
}

async function fetchPlaces(token) {
    /* التعديل 1: الرابط الديناميكي لبيئة Codespaces */
    let baseUrl = window.location.origin.replace('-3000', '-5000').replace('-8080', '-5000');
    if (baseUrl.includes('localhost') || baseUrl.includes('127.0.0.1')) {
        baseUrl = 'http://127.0.0.1:5000';
    }
    
    const API_URL = `${baseUrl}/api/v1/places/`; // تأكد من وجود الـ slash في النهاية

    try {
        const headers = {};
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        const response = await fetch(API_URL, { headers });
        
        if (response.ok) {
            const data = await response.json();
            displayPlaces(data);
        } else {
            console.error('Failed to fetch places:', response.statusText);
        }
    } catch (error) {
        console.error('Error fetching places:', error);
    }
}

function displayPlaces(places) {
    const placesList = document.getElementById('places-list');
    if (!placesList) return;

    placesList.innerHTML = '';

    places.forEach(place => {
        const card = document.createElement('div');
        card.className = 'place-card';
        card.dataset.price = place.price;
        
        /* التعديل 2: استخدمنا title و price و description كما في قاعدة بياناتنا */
        // ملاحظة: إذا كان الـ API يرجع "title" نستخدمه، وإذا يرجع "name" نستخدمه كبديل
        const displayTitle = place.title || place.name || 'No Title';
        
        card.innerHTML = `
            <div class="place-info">
                <h2>${displayTitle}</h2>
                <p class="price"><strong>Price per night:</strong> $${place.price}</p>
                <p class="description">${place.description || 'No description available.'}</p>
                <a href="place.html?id=${place.id}" class="details-button">View Details</a>
            </div>
        `;
        placesList.appendChild(card);
    });
}

document.addEventListener('DOMContentLoaded', () => {
    checkAuthentication();

    const priceFilter = document.getElementById('price-filter');
    if (priceFilter) {
        priceFilter.addEventListener('change', (event) => {
            const selected = event.target.value;
            const cards = document.querySelectorAll('.place-card');

            cards.forEach(card => {
                const price = parseFloat(card.dataset.price);
                if (selected === 'all' || price <= parseFloat(selected)) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    }
});
