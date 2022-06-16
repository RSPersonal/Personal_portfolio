import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import { BootstrapVue, IconsPlugin } from "bootstrap-vue"
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap";
import axios from "axios";
import VueAxios from "vue-axios";

const app = createApp(App);

app.use(VueAxios, axios);
app.use(BootstrapVue);
app.use(IconsPlugin);
app.use(router);

app.mount("#app");

if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/sw.js');
    });
}
