<template>
  <div class="user-navbar my-2">
    <div class="left">
      <p style="font-size: 20px"><b>Ticket Show</b></p>
    </div>
    <div class="right">
      <div class="profile mx-3 btn">
        <span class="material-symbols-outlined btn px-1"> person </span>
        <span
          ><b>{{ user }}</b></span
        >
      </div>
      <router-link
        class="btn btn-sm btn-secondary mx-1"
        :to="{ name: 'UserDashBoard' }"
        >Home</router-link
      >
      <router-link
        class="btn btn-sm btn-secondary mx-1"
        :to="{ name: 'AllShows' }"
        >Shows</router-link
      >
      <router-link
        :to="{ name: 'SearchBar' }"
        class="btn btn-sm btn-secondary mx-1"
        >Search</router-link
      >
      <router-link
        class="mx-1 btn btn-sm btn-secondary"
        :to="{ name: 'UserBookings' }"
      >
        My Bookings</router-link
      >
      <button class="btn btn-danger btn-sm mx-1" @click.prevent="logout">
        Logout
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: "UserNavbar",
  data() {
    return {
      user: localStorage.getItem("name")
    };
  },
  methods: {
    logout() {
      this.$router.push({ name: "UserLogin" });
      localStorage.clear();
      alert("Logged Out Successfully");
    },
  },
};
</script>

<style scoped>
.user-navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.user-navbar .right {
  display: flex;
  justify-content: space-evenly;
  align-items: center;
}
</style>
