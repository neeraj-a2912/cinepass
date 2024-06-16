<template>
  <div class="container">
    <NavbarHome />
    <div class="content">
      <h1 class="mt-5">Welcome to Ticket Show</h1>
      <img
        src="../assets/movieticket.jpg"
        class="rounded w-50"
        alt="ticket counter"
      /><br/>
      <router-link class="btn btn-danger" :to="{ name: 'RegisterForm' }">Create an Account -></router-link>
    </div>
  </div>
</template>

<script>
import NavbarHome from "./NavbarHome.vue";
export default {
  name: "LandingPage",
  components: { NavbarHome },
};
</script>

<style>
.content {
  text-align: center;
}
.content img{
    height: 400px;
    width: 300px;
}
</style>
