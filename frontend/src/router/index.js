import { createRouter, createWebHistory } from "vue-router";
import HomeViewEN from "../views/HomepageEN.vue";
import HomeViewNL from "../views/HomepageNL.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "homeEn",
      component: HomeViewEN,
    },
    {
      path: "/nl",
      name: "homeNl",
      component: HomeViewNL,
    },
    {
      path: "/about",
      name: "about",
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import("../views/AboutView.vue"),
    },
  ],
});

export default router;
