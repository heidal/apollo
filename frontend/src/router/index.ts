import Vue from "vue";
import VueRouter from "vue-router";
import Login from "../views/Login.vue";
import Logout from "../views/Logout.vue";
import Signup from "../views/Signup.vue";
import LandingPage from "../views/LandingPage.vue";
import ElectionCreationPage from "../views/ElectionCreationPage.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "Home",
    component: LandingPage
  },
  {
    path: "/login",
    name: "Login",
    component: Login
  },
  {
    path: "/logout",
    name: "Logout",
    component: Logout
  },
  {
    path: "/signup",
    name: "Signup",
    component: Signup
  },
  {
    path: "/create-election",
    name: "Create Election",
    component: ElectionCreationPage,
  }
];

const router = new VueRouter({
  routes,
  mode: "history"
});

export default router;
