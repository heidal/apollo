import Vue from "vue";
import VueRouter, { Route } from "vue-router";
import Login from "@/views/Login.vue";
import Logout from "@/views/Logout.vue";
import Signup from "@/views/Signup.vue";
import LandingPage from "@/views/LandingPage.vue";
import ElectionCreationPage from "@/views/ElectionCreationPage.vue";
import ElectionEditionPage from "@/views/ElectionEditionPage.vue";
import ElectionsPage from "@/views/ElectionsPage.vue";
import ElectionDetailPage from "@/views/ElectionDetailPage.vue";
import ElectionResults from "@/views/ElectionResults.vue";
import VotePage from "@/views/VotePage.vue";
import BulletinBoardPage from "@/views/BulletinBoardPage.vue";

import store from "@/store";

Vue.use(VueRouter);

const authenticatedRouteGuard = (
  to: Route,
  from: Route,
  next: CallableFunction
) => {
  if (!store.getters.isAuthenticated)
    next({ name: "Login", query: { next: to.path } });
  else next();
};

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
    path: "/elections",
    name: "Elections list",
    component: ElectionsPage
  },
  {
    path: "/election-detail/:electionId",
    name: "Election detail",
    component: ElectionDetailPage
  },
  {
    path: "/election-detail/:electionId/results",
    name: "Election results",
    component: ElectionResults
  },
  {
    path: "/bulletin-board/:electionId",
    name: "Bulletin board",
    component: BulletinBoardPage
  },
  {
    path: "/create-election",
    name: "Create Election",
    component: ElectionCreationPage,
    beforeEnter: authenticatedRouteGuard
  },
  {
    path: "/edit-election/:electionId",
    name: "Edit election",
    component: ElectionEditionPage,
    beforeEnter: authenticatedRouteGuard
  },
  {
    path: "/vote/:electionId",
    name: "Vote in Election",
    component: VotePage,
    beforeEnter: authenticatedRouteGuard
  }
];

const router = new VueRouter({
  routes,
  mode: "history"
});

export default router;
