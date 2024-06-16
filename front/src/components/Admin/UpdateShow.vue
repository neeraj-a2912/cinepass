<template>
  <div class="container my-0">
    <AdminNavbar/>
    <form @submit.prevent="updateShow" action="">
      <label for="name" >Name</label>
      <input
        type="text"
        class="form-control form-control-sm shadow-none"
        name="name"
        v-model="formData.name"
      />
      <label for="tags" >Tags</label>
      <input
        type="text"
        class="form-control form-control-sm shadow-none"
        name="tags"
        v-model="formData.tags"
      />
      <label for="ticket_price" >Ticket Price</label>
      <input
        type="number"
        class="form-control form-control-sm shadow-none"
        name="ticket_price"
        v-model="formData.ticket_price"
      />
      <label for="capacity" >Available Seats</label>
      <input
        type="number"
        class="form-control form-control-sm shadow-none"
        name="capacity"
        v-model="formData.capacity"
      />
      <label for="ratings" >Ratings</label>
      <input
        type="number"
        class="form-control form-control-sm shadow-none"
        name="ratings"
        v-model="formData.ratings"
      />
      <label  for="screen_number">Screen Number</label>
      <input
        type="number"
        class="form-control form-control-sm shadow-none"
        name="screen_number"
        v-model="formData.screen_number"
        required
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
      <button class="btn btn-secondary">Update</button>
    </form>
  </div>
</template>

<script>
import AdminNavbar from './AdminNavbar.vue'
export default {
  name: "UpdateShow",
  components:{ AdminNavbar },
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
        show_date:""
      },
    };
  },
  mounted() {
    this.showDetails();
  },
  methods: {
    async updateShow() {
      console.log("edit show clicked");
      const response = await fetch(
        `http://localhost:5000/api/show/${this.$route.params.theatre_id}/${this.$route.params.show_id}`,
        {
          method: "PUT",
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
          alert("Show Updated Successfully");
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
        this.formData = data;
      }
    },
  },
};
</script>

