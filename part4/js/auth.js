document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');

    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            
            // استخدام selector دقيق لجلب القيم
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;

            // تحديد رابط الـ API (تأكد من تغيير localhost إذا كنت تستخدم السيرفر عن بعد)
            const API_URL = 'http://127.0.0.1:5000/api/v1/auth/login';

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
                    
                    /* تحسين تخزين الكوكي:
                       - path=/ : لجعل الكوكي متاحاً في كل الصفحات.
                       - max-age : ليبقى مسجلاً لمدة 24 ساعة.
                       - SameSite=Lax : لضمان الأمان وتوافق المتصفحات الحديثة.
                    */
                    document.cookie = `token=${data.access_token}; path=/; max-age=86400; SameSite=Lax`;
                    
                    // تحويل المستخدم للصفحة الرئيسية
                    window.location.href = 'index.html';
                } else {
                    // محاولة قراءة رسالة الخطأ القادمة من السيرفر (مثل "Invalid password")
                    const errorData = await response.json().catch(() => ({}));
                    alert('Login failed: ' + (errorData.message || 'Invalid credentials'));
                }
            } catch (error) {
                console.error('Fetch Error:', error);
                alert('Connection error: Please check if the API server is running.');
            }
        });
    }
});
