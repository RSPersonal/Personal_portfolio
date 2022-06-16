<script setup>
import { RouterView } from "vue-router";
import NavBar from "@/components/NavBar.vue";
import BaseFooter from "@/components/BaseFooter.vue";
</script>

<template>
  <NavBar />
  <RouterView />
  <BaseFooter />
</template>

<style>
@import "./assets/style.css";
</style>
