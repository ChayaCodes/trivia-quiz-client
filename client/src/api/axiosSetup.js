import axios from 'axios';
import createAuthRefreshInterceptor from 'axios-auth-refresh';

// יצירת אינסטנס של Axios
const api = axios.create({
    baseURL: 'http://localhost:5000',
    withCredentials: true // מאפשר שילוב קוקיז בבקשות
});

// פונקציה לחידוש הטוקן
const refreshAuthLogic = failedRequest =>
    api.post('/auth/refresh')
        .then(response => {
            // הטוקן החדש כבר נשמר כקוקיז, ניתן להמשיך בבקשה המקורית
            failedRequest.response.config.withCredentials = true;
            return Promise.resolve();
        })
        .catch(err => {
            // טיפול בשגיאה אם החידוש נכשל
            return Promise.reject(err);
        });

// יצירת אינטרספטור
createAuthRefreshInterceptor(api, refreshAuthLogic);

export default api;