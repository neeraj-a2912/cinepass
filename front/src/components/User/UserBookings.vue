<template>
  <div class="container">
    <UserNavbar />
    <div v-for="booking in bookings" class="m-2" :key="booking.id">
      <div class="name-time">
        <h5>
          <b>{{ booking.name }}</b>
        </h5>
      </div>
      <p class="m-0">
        Date and Time :
        <b>{{ booking.show_date }}, {{ booking.show_timing }}</b>
      </p>
      <p class="m-0">Number of tickets : {{ booking.number_of_tickets }}</p>
      <div class="theatre-screen">
        <p>
          <b
            >Screen {{ booking.screen }}, {{ booking.theatre }},
            {{ booking.location }}</b
          >
        </p>
        <b>Total Amount : Rs. {{ booking.total_price }}</b>
      </div>
    </div>
  </div>
</template>

<script>
import UserNavbar from "./UserNavbar.vue";
export default {
  name: "UserBookings",
  components: {
    UserNavbar,
  },
  data() {
    return {
      bookings: [],
      user: {},
    };
  },
  mounted() {
    this.getBookings();
  },
  methods: {
    async getBookings() {
      const response = await fetch(
        `http://localhost:5000/api/bookings/user/${localStorage.getItem(
          "user_id"
        )}`,
        {
          method: "GET",
          headers: {
            Authorization: "Bearer " + localStorage.getItem("access-token"),
          },
        }
      );
      const data = await response.json();
      if (response.ok) {
        this.bookings = data;
      }
    },
  },
};
</script>

<style scoped>
.name-time,
.theatre-screen {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
