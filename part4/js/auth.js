document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-link'); // تأكد أن ID الفورم في login.html هو login-form
    const formElement = document.getElementById('login-form');

    if (formElement) {
        formElement.addEventListener('submit', async (event) => {
            event.preventDefault();
            
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;

            // دالة اكتشاف رابط الباك اند تلقائياً
            const getBaseUrl = () => {
                const { origin } = window.location;
                if (origin.includes('github.dev') || origin.includes('app.github.dev')) {
                    return origin.replace(/-(3000|5500|8080)\./, '-5000.');
                }
                return 'http://127.0.0.1:5000';
            };

            const API_URL = `${getBaseUrl()}/api/v1/login`;

            try {
                const response = await fetch(API_URL, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ email, password })
                });

                if (response.ok) {
                    const data = await response.json();
                    
                    /* التعليمات الصارمة: تخزين التوكن في الكوكيز */
                    // نقوم بضبط الكوكي ليعمل على كامل الموقع لمدة 24 ساعة
                    document.cookie = `token=${data.access_token}; path=/; max-age=86400; SameSite=Lax`;
                    
                    // اختيارياً للمساعدة في العمليات السريعة
                    localStorage.setItem('token', data.access_token);
                    
                    window.location.href = 'index.html';
                } else {
                    const errorData = await response.json().catch(() => ({}));
                    alert('Login failed: ' + (errorData.msg || errorData.message || 'Invalid credentials'));
                }
            } catch (error) {
                console.error('Fetch Error:', error);
                alert('Connection error: Make sure your Python server is running.');
            }
        });
    }
});
