<template>
  <div class="user-navbar my-2">
    <div class="left">
      <p style="font-size: 20px;"><b>Ticket Show</b></p>
    </div>
    <div class="right">
      <router-link class="btn btn-sm btn-secondary" :to="{ name: 'AdminLogin' }">Admin Login</router-link>
      <router-link class="mx-2 btn btn-danger btn-sm" :to="{ name: 'UserLogin' }">
        User Login</router-link
      >
    </div>
  </div>
</template>

<script>
export default {
    name:"NavbarHome"
}
</script>

<style>
a{
    text-decoration: none;
    color: white;
}
</style>