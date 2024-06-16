<template>
  <div class="user-navbar my-2">
    <div class="left">
      <p style="font-size: 20px;"><b>Ticket Show</b></p>
    </div>
    <div class="right">
      <router-link class="btn btn-sm btn-secondary mx-1" :to="{ name: 'AdminDashBoard' }">Home</router-link>
      <button class="btn btn-danger btn-sm mx-1" @click.prevent="logout">
        Logout
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: "AdminNavbar",
  methods: {
    logout() {
      this.$router.push({ name: "UserLogin" });
      localStorage.clear();
      alert("Logged Out Successfully");
    },
  },
};
</script>

<style scoped></style>
