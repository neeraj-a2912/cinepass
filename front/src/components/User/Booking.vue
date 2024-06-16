<template>
  <div class="container mt-2">
    <UserNavbar />
    <div class="show-details my-4">
      <table class="table table-borderless">
        <tbody>
          <tr>
            <td scope="col"><b>Movie</b></td>
            <td scope="col">{{ show.name }}</td>
          </tr>
          <tr>
            <td scope="col"><b>Tags</b></td>
            <td scope="col">{{ show.tags }}</td>
          </tr>
          <tr>
            <td scope="col"><b>Ratings</b></td>
            <td scope="col">{{ show.ratings }}/5</td>
          </tr>
          <tr>
            <td scope="col"><b>Ticket Price</b></td>
            <td scope="col">{{ show.ticket_price }}</td>
          </tr>
          <tr>
            <td scope="col"><b>Screen</b></td>
            <td scope="col">{{ show.screen_number }}</td>
          </tr>
        </tbody>
      </table>
      <h4 style="text-align: center" class="mt-3">
        Total Price : {{ formData.number_of_tickets * show.ticket_price }}
      </h4>
    </div>
    <form @submit.prevent="bookShow">
      <label for="ticketCount">Number of Seats</label><br />
      <input
        class="form-control form-control-sm shadow-none"
        type="number"
        name="ticketCount"
        v-model="formData.number_of_tickets"
        min="1"
        :max="show.capacity"
        required
      /><br />
      <button class="btn btn-sm btn-danger">Confirm Booking</button>
    </form>
  </div>
</template>

<script>
import UserNavbar from "./UserNavbar.vue";
export default {
  name: "BookingItem",
  components: { UserNavbar },
  data() {
    return {
      formData: {
        user_id: localStorage.getItem("user_id"),
        number_of_tickets: 1,
      },
      show: {},
    };
  },
  mounted() {
    this.showDetails();
  },
  methods: {
    async bookShow() {
      const response = await fetch(
        `http://localhost:5000/api/booking/${this.$route.params.show_id}`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            Authorization: "Bearer " + localStorage.getItem("access-token"),
          },
          body: JSON.stringify(this.formData),
        }
      );
      const data = await response.json();
      if (response.ok) {
        console.log(data);
        console.log(this.formData);
        this.$router.push({ name: "BookingConfirm" });
      }
    },
    async showDetails() {
      const response = await fetch(
        `http://localhost:5000/api/show-details/${this.$route.params.show_id}`,
        {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            Authorization: "Bearer " + localStorage.getItem("access-token"),
          },
        }
      );
      const data = await response.json();
      if (response.ok) {
        console.log(data);
        this.show = data;
      }
    },
  },
};
</script>

<style>
.show-details {
  width: 50%;
  margin: 20px auto;
  padding: 10px;
}
</style>
