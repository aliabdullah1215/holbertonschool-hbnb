document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');

    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;

            /* التعديل 1: تحديد رابط الـ API بشكل ديناميكي.
               في Codespaces، نستخدم الرابط الذي ينتهي بـ -5000.app.github.dev
               الكود أدناه يحاول اكتشاف الرابط تلقائياً، وإذا فشل يعود للـ localhost.
            */
            let baseUrl = window.location.origin.replace('-3000', '-5000').replace('-8080', '-5000');
            if (baseUrl.includes('localhost') || baseUrl.includes('127.0.0.1')) {
                baseUrl = 'http://127.0.0.1:5000';
            }
            
          // هذا الكود يكتشف أين يعمل الفرونت اند ويخمن رابط الباك اند تلقائياً
const getBaseUrl = () => {
    const { origin } = window.location;
    
    // إذا كنت في Codespaces، سيقوم بتبديل منفذ الفرونت اند (3000 أو 5500) بمنفذ الباك اند (5000)
    if (origin.includes('github.dev') || origin.includes('app.github.dev')) {
        return origin.replace(/-(3000|5500|8080)\./, '-5000.');
    }
    
    // إذا كنت تعمل محلياً على جهازك
    return 'http://127.0.0.1:5000';
};

const API_URL = `${getBaseUrl()}/api/v1`;

                if (response.ok) {
                    const data = await response.json();
                    
                    // التعديل 2: تخزين التوكن في الكوكيز وفي localStorage لضمان التوافق مع باقي ملفات JS
                    document.cookie = `token=${data.access_token}; path=/; max-age=86400; SameSite=Lax`;
                    localStorage.setItem('token', data.access_token);
                    
                    alert('Login successful! Redirecting...');
                    window.location.href = 'index.html';
                } else {
                    const errorData = await response.json().catch(() => ({}));
                    alert('Login failed: ' + (errorData.msg || errorData.message || 'Invalid email or password'));
                }
            } catch (error) {
                console.error('Fetch Error:', error);
                alert('Connection error: Make sure your Python server is running on port 5000.');
            }
        });
    }
});

// دالة مساعدة قد نحتاجها في ملفات JS الأخرى لجلب التوكن من الكوكيز
function getTokenFromCookie() {
    const name = "token=";
    const decodedCookie = decodeURIComponent(document.cookie);
    const ca = decodedCookie.split(';');
    for(let i = 0; i < ca.length; i++) {
        let c = ca[i].trim();
        if (c.indexOf(name) == 0) return c.substring(name.length, c.length);
    }
    return "";
}
