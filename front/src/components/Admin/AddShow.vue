<template>
  <div class="container my-0">
    <AdminNavbar />
    <div class="add-show">
      <form @submit.prevent="addShow" action="">
        <h3>Add New Show</h3>
        <label for="name">Name</label>
        <input
          type="text"
          class="form-control form-control-sm shadow-none"
          name="name"
          v-model="formData.name"
          required
        />
        <label for="tags">Tags</label>
        <input
          type="text"
          class="form-control form-control-sm shadow-none"
          name="tags"
          v-model="formData.tags"
          required
        />
        <label for="ticket_price">Ticket Price</label>
        <input
          type="number"
          name="ticket_price"
          v-model="formData.ticket_price"
          class="form-control form-control-sm shadow-none"
          min="100"
          required
        />
        <label for="capacity">Available Seats</label>
        <input
          type="number"
          name="capacity"
          v-model="formData.capacity"
          class="form-control form-control-sm shadow-none"
          min="20"
          required
        />
        <label for="ratings">Ratings</label>
        <input
          type="number"
          name="ratings"
          v-model="formData.ratings"
          class="form-control form-control-sm shadow-none"
          min="0"
          max="5"
          required
        />
        <label for="screen_number">Screen Number</label>
        <input
          type="number"
          class="form-control form-control-sm shadow-none"
          name="screen_number"
          v-model="formData.screen_number"
          required
          min="1"
          max="7"
        />
        <label for="show_date">Date</label>
        <input
          type="date"
          class="form-control form-control-sm shadow-none"
          name="show_date"
          v-model="formData.show_date"
          required
        />

        <label for="show_timing">Time</label>
        <select
          name="show_timing"
          v-model="formData.show_timing"
          required
          class="form-control form-control-sm shadow-none"
        >
          <option value="11:00 AM - 2:00 PM">11:00 AM - 2:00 PM</option>
          <option value="2:00 PM - 5:00 PM">2:00 PM - 5:00 PM</option>
          <option value="6:00 PM - 9:00 PM">6:00 PM - 9:00 PM</option>
          <option value="9:00 PM - 12:00 AM">9:00 PM - 12:00 AM</option></select
        ><br />
        <button class="btn btn-secondary">Add Show</button>
      </form>
    </div>
  </div>
</template>

<script>
import AdminNavbar from "./AdminNavbar.vue";
export default {
  name: "AddShow",
  components: { AdminNavbar },
  data() {
    return {
      formData: {
        name: "",
        tags: "",
        ratings: "",
        ticket_price: 100,
        capacity: 20,
        screen_number: 0,
        show_timing: "",
        show_date: "",
      },
    };
  },
  methods: {
    async addShow() {
      console.log("add show clicked");
      const response = await fetch(
        `http://localhost:5000/api/show/${this.$route.params.theatre_id}`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: "Bearer " + localStorage.getItem("access-token"),
          },
          body: JSON.stringify(this.formData),
        }
      );
      if (response.status != 409) {
        const data = await response.json();
        if (response.ok) {
          console.log(response);
          alert("Show Added Successfully");
          return this.$router.push({
            name: "AdminShows",
            params: { theatre_id: this.$route.params.theatre_id },
          });
        } else {
          alert(data.error_message);
        }
      } else {
        alert("show already exists");
      }
    },
  },
};
</script>

<style>
.add-show {
  width: 80%;
  margin: 4px auto;
}
form {
  width: 50%;
  margin: 8px auto;
  /* box-shadow: rgba(0, 0, 0, 0.16) 0px 1px 4px; */
  padding: 10px;
}
</style>
