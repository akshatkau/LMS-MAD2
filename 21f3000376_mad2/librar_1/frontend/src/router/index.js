import { createRouter, createWebHistory } from 'vue-router';
import store from '../store';
import HomeView from '../views/HomeView.vue';
import UserSignUp from '../views/UserSignUp.vue';
import LoginUser from '../views/LoginUser.vue';
import UserDashboard from '../views/UserDashboard.vue';
import AdminDashboard from '../views/AdminDashboard.vue';
import SectionManagement from '../views/SectionManagement.vue';
import SectionBooks from '../views/SectionBooks.vue';
import UserBooks from '../views/UserBooks.vue';
import UserRequests from '../views/UserRequests.vue';
import AdminRequests from '../views/AdminRequests.vue';
import BookFeedbacks from '../views/BookFeedbacks.vue';
import AdminStats from '../views/AdminStats.vue';
import PaymentPage from '../views/PaymentPage.vue';
import BookContent from '../views/BookContent.vue';

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/book-content/:bookId',
    name: 'BookContent',
    component: BookContent,
  },
  {
    path: '/payment/:bookId',
    name: 'PaymentPage',
    component: PaymentPage,
    props: true
  },
  {
    path: '/admin-stats',
    name: 'admin-stats',
    component: AdminStats
  },
  {
    path: '/feedbacks/:bookId',
    name: 'BookFeedbacks',
    component: BookFeedbacks,
    props: true
  },
  {
    path: '/section/:sectionId',
    name: 'section-books',
    component: SectionBooks,
    meta: { requiresAuth: true, roles: ['admin'] }
  },
  {
    path: '/section',
    name: 'section',
    component: SectionManagement,
    meta: { requiresAuth: true, roles: ['admin'] }
  },
  {
    path: '/admin-requests',
    name: 'admin-requests',
    component: AdminRequests,
    meta: { requiresAuth: true, roles: ['admin'] }
  },

  {
    path: '/admin-dashboard',
    name: 'admin-dashboard',
    component: AdminDashboard,
    meta: { requiresAuth: true, roles: ['admin'] }
  },
  {
    path: '/login',
    name: 'login',
    component: LoginUser,
    meta: { requiresGuest: true }
  },
  {
    path: '/signup',
    name: 'signup',
    component: UserSignUp,
    meta: { requiresGuest: true }
  },
  {
    path: '/user-dashboard',
    name: 'user-dashboard',
    component: UserDashboard,
    meta: { requiresAuth: true, roles: ['user'] }
  },
  {
    path: '/user-books',
    name: 'user-books',
    component: UserBooks,
    meta: { requiresAuth: true, roles: ['user'] }
  },
  {
    path: '/user-requests',
    name: 'user-requests',
    component: UserRequests,
    meta: { requiresAuth: true, roles: ['user'] }
  },
  
  {
    path: '/about',
    name: 'about',
    component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  }
];

const router = createRouter({
  history: createWebHistory(),  // Ensure this matches your setup
  routes
});

router.beforeEach((to, from, next) => {
  if (to.meta.requiresAuth) {
    if (!store.getters.isAuthenticated) {
      next('/login');
    } else {
      const userRole = store.getters.userRole;
      if (to.meta.roles && !to.meta.roles.includes(userRole)) {
        next('/');
      } else {
        next();
      }
    }
  } else if (to.meta.requiresGuest && store.getters.isAuthenticated) {
    next('/');
  } else {
    next();
  }
});

export default router;
