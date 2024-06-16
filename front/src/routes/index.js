import * as VueRouter from "vue-router";
import RegisterForm from "../components/RegisterForm.vue";
import LandingPage from "../components/LandingPage.vue";

// Admin Components
import AdminLogin from "../components/Admin/AdminLogin.vue";
import AdminDashBoard from "../components/Admin/AdminDashBoard.vue";
import AddTheatre from "../components/Admin/AddTheatre.vue";
import AddShow from "../components/Admin/AddShow.vue";
import UpdateShow from "../components/Admin/UpdateShow.vue";
import UpdateTheatre from "../components/Admin/UpdateTheatre.vue";
import AdminShows from "../components/Admin/Shows.vue";

// User Components
import UserLogin from "../components/User/UserLogin.vue";
import UserDashBoard from "../components/User/UserDashBoard.vue";
import TheatreDetails from "../components/User/TheatreDetails.vue";
import BookingItem from "../components/User/Booking.vue";
import BookingConfirm from "../components/User/BookingConfirm.vue";
import UserBookings from "../components/User/UserBookings.vue";
import SearchBar from "../components/User/SearchBar.vue";
import AllShows from "../components/User/AllShows.vue"
const routes = [
  {
    path: "/register",
    name: "RegisterForm",
    component: RegisterForm,
  },
  {
    path: "/",
    name: "LandingPage",
    component: LandingPage,
  },
  // Admin Routes
  {
    path: "/admin/login",
    name: "AdminLogin",
    component: AdminLogin,
  },
  {
    path: "/admin",
    name: "AdminDashBoard",
    component: AdminDashBoard,
    meta: {
      requiresAuth: true,
      requiresAdmin: true,
    },
  },
  {
    path: "/admin/addnewtheatre",
    name: "AddTheatre",
    component: AddTheatre,
    meta: {
      requiresAuth: true,
      reuiresAdmin: true,
    },
  },
  {
    path: "/admin/shows/theatre-id/:theatre_id",
    name: "AdminShows",
    component: AdminShows,
    meta: {
      requiresAuth: true,
      requiresAdmin: true,
    },
  },
  {
    path: "/admin/theatre/:theatre_id/addnewshow",
    name: "AddShow",
    component: AddShow,
    meta: {
      requiresAuth: true,
      requiresAdmin: true,
    },
  },
  {
    path: "/admin/update-show/:theatre_id/:show_id",
    name: "UpdateShow",
    component: UpdateShow,
    meta: {
      requiresAuth: true,
      requiresAdmin: true,
    },
  },
  {
    path: "/admin/update-theatre/:theatre_id",
    name: "UpdateTheatre",
    component: UpdateTheatre,
    meta: {
      requiresAuth: true,
      requiresAdmin: true,
    },
  },
  // User Routes
  {
    path: "/user/login",
    name: "UserLogin",
    component: UserLogin,
    meta: {
      requiresAuth: false,
    },
  },
  {
    path: "/user",
    name: "UserDashBoard",
    component: UserDashBoard,
    meta: {
      requiresAuth: true,
    },
  },
  {
    path: "/all-shows",
    name: "AllShows",
    component: AllShows,
    meta: {
      requiresAuth: true,
    },
  },
  {
    path: "/user/now-showing/theatre-id/:theatre_id",
    name: "TheatreDetails",
    component: TheatreDetails,
    meta: {
      requiresAuth: true,
    },
  },
  {
    path: "/user/search-shows-or-theatres",
    name: "SearchBar",
    component: SearchBar,
    meta: {
      requiresAuth: true,
    },
  },
  {
    path: "/user/booking/:show_id",
    name: "BookingItem",
    component: BookingItem,
    meta: {
      requiresAuth: true,
    },
  },
  {
    path: "/user/booking/status-confirmed",
    name: "BookingConfirm",
    component: BookingConfirm,
    meta: {
      requiresAuth: true,
    },
  },
  {
    path: "/user/mybookings",
    name: "UserBookings",
    component: UserBookings,
    meta: {
      requiresAuth: true,
    },
  },
];

const router = new VueRouter.createRouter({
  history: VueRouter.createWebHistory(),
  routes,
});

function isAuthenticated() {
  if (localStorage.getItem("access-token")) {
    return true;
  }
  return false;
}

function isAdmin() {
  if (localStorage.getItem("role") === "admin") {
    return true;
  }
  return false;
}

router.beforeEach((to, from, next) => {
  console.log(from);
  if (to.meta.requiresAuth && !isAuthenticated()) {
    next("/user/login");
  } else if (to.meta.requiresAuth && isAuthenticated()) {
    if (to.meta.requiresAdmin && !isAdmin()) {
      next('/user');
    } else {
      next();
    }
  } else {
    next();
  }
});

export default router;
