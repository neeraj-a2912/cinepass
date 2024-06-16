<template>
  <div class="container mt-2">
    <UserNavbar />
    <div class="theatre-items">
      <TheatreItem
        v-for="theatre in theatres"
        :key="theatre.id"
        :tname="theatre.name"
        :place="theatre.place"
        :capacity="theatre.capacity"
        :id="theatre.id"
      />
    </div>
  </div>
</template>

<script>
import TheatreItem from "./TheatreItem.vue";
import UserNavbar from "./UserNavbar.vue";
export default {
  name: "UserDashBoard",
  components: {
    TheatreItem,
    UserNavbar,
  },
  data() {
    return {
      theatres: [],
    };
  },
  mounted() {
    this.getTheatreList();
  },
  methods: {
    async getTheatreList() {
      const response = await fetch("http://localhost:5000/api/theatre", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          "Access-Control-Allow-Origin": "*",
          Authorization: "Bearer " + localStorage.getItem("access-token"),
        },
      });
      const data = await response.json();
      if (response.ok) {
        this.theatres = data;
      }
    },
  },
};
</script>

<style>
.user-navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.user-navbar .left a {
  text-decoration: none;
}
.container .theatre-items {
  display: flex;
  flex-wrap: wrap;
}
</style>
