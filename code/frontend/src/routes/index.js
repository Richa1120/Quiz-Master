import jwt_decode from "jwt-decode";
import Vue from "vue";
import VueRouter from "vue-router";

// Import User Components
import chaptersPage from "../components/chaptersPage.vue";
import quizPage from "../components/quizPage.vue";
import quizzesPage from "../components/quizzesPage.vue";
import userPerformance from "../components/userPerformance.vue";
import userQuizHistory from "../components/userQuizHistory.vue";

// Import Admin Components
import adminChapters from "../components/adminChapters.vue";
import adminDashboard from "../components/adminDashboard.vue";
import adminExports from "../components/adminExports.vue";
import adminLogin from "../components/adminLogin.vue";
import adminQuestions from "../components/adminQuestions.vue";
import adminQuizzes from "../components/adminQuizzes.vue";
import adminSubjects from "../components/adminSubjects.vue";
import adminUsers from "../components/adminUsers.vue";

// Import Views
import LandingPage from "../view/LandingPage.vue";
import LoginView from "../view/LoginView.vue";
import SignUpView from "../view/SignUpView.vue";
import homePageView from "../view/homePageView.vue";

Vue.use(VueRouter);

const routes = [
    { path: "/", name: "LandingPage", component: LandingPage },

    // User Routes
    { path: "/register", name: "SignUp", component: SignUpView },
    { path: "/login", name: "Login", component: LoginView },
    { path: "/home", name: "home", component: homePageView, meta: { requiresAuth: true } },
    { path: "/user/quiz/:quizId", name: "quizPage", component: quizPage, meta: { requiresAuth: true }},
    { path: "/user/quiz-history", name: "userQuizHistory", component: userQuizHistory, meta: {requiresAuth: true}},
    { path: "/user/performance", name: "userPerformance", component: userPerformance, meta: {requiresAuth: true}},
    { path: "/user/chapters/:subjectId", name: "chaptersPage", component: chaptersPage, meta: {requiresAuth: true}},
    { path: "/user/quizzes/:chapterId", name: "quizzesPage", component: quizzesPage, meta: {requiresAuth: true}},

    // Admin Routes
    { path: "/admin/login", name: "adminLogin", component: adminLogin },
    { path: "/admin/dashboard", name: "adminDashboard", component: adminDashboard, meta: { requiresAuth: true, requiresAdmin: true } },
    { path: "/admin/subjects", name: "adminSubjects", component: adminSubjects, meta: { requiresAuth: true, requiresAdmin: true } },
    { path: "/admin/quizzes", name: "adminQuizzes", component: adminQuizzes, meta: { requiresAuth: true, requiresAdmin: true}},
    { path: "/admin/users", name: "adminUsers", component: adminUsers, meta: { requiresAuth: true, requiresAdmin: true } }, // Updated Route
    { path: "/admin/chapters", name: "adminChapters", component: adminChapters, meta: { requiresAuth: true, requiresAdmin: true } },
    { path: "/admin/quiz/:quizId/questions", name: "adminQuestions", component: adminQuestions, meta: { requiresAuth: true, requiresAdmin: true }},
    { path: "/admin/exports", name: "adminExports", component: adminExports, meta: { requiresAuth: true, requiresAdmin: true }},
]

const router = new VueRouter({
    mode: 'history',
    base: process.env.BASE_URL,
    routes
})



function verifyToken(token){
    try{
        const decoded = jwt_decode(token)
        console.log(decoded)
        return decoded
    }catch(error){
        console.error(error)
        return null
    }
}

router.beforeEach((to, from, next)=> {
    const isAuthenticated = localStorage.getItem('token')
    const isAdmin = localStorage.getItem('user_type') === 'admin'
    const isUser = localStorage.getItem('user_type') === 'user'

    if(to.matched.some(record => record.meta.requiresAuth)){
        if(isAuthenticated === 'null'){
            alert('Please Login to continue')
            next({path: '/'})
        }else{
            try{
                const decodedToken = verifyToken(isAuthenticated)
                if(decodedToken && decodedToken.exp * 1000 > Date.now()){
                    if(to.matched.some(record => record.meta.requiresAdmin)&& !isAdmin){
                        alert('Only Admins can access');
                        localStorage.setItem('token','null');
                        localStorage.setItem('user_type','null');
                        next({path: '/'})
                    }else if(to.matched.some(record => record.meta.notUser)&& isUser){
                        alert('Users cannot access');
                        localStorage.setItem('token','null');
                        localStorage.setItem('user_type','null');
                        next({path: '/'})
                    }else{
                        next()
                    }
                }else{
                    alert('Session expired!!')
                    next({path: '/'})
                }
            }catch(error){
                console.error(error)
                next({path: '/'})
            }
        }
    }else{
        next()
    }
})

export default router;

