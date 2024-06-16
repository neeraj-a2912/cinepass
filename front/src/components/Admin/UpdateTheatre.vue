<template>
  <div class="container my-0">
    <AdminNavbar />
    <form @submit.prevent="updateTheatre" action="">
      <label for="name">Name</label><br />
      <input
        type="text"
        class="form-control form-control-sm shadow-none"
        name="name"
        v-model="formData.name"
      /><br />
      <label for="place">Place</label><br />
      <input
        type="text"
        class="form-control form-control-sm shadow-none"
        name="place"
        v-model="formData.place"
      /><br />
      <label for="screens">Screens</label><br />
      <input
        type="number"
        name="screens"
        class="form-control form-control-sm shadow-none"
        v-model="formData.screens"
        min="0"
      /><br />
      <button class="btn btn-secondary">Update</button>
    </form>
  </div>
</template>

<script>
import AdminNavbar from "./AdminNavbar.vue";
export default {
  name: "UpdateTheatre",
  components: { AdminNavbar },
  data() {
    return {
      formData: {
        name: "",
        place: "",
        screens: "",
      },
    };
  },
  mounted() {
    this.theatreDetails();
  },
  methods: {
    async updateTheatre() {
      console.log("add theatre clicked");
      const response = await fetch(
        `http://localhost:5000/api/theatre/${this.$route.params.theatre_id}`,
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
          return this.$router.push({ name: "AdminDashBoard" });
        } else {
          alert(data.error_message);
        }
      } else {
        alert("Please Use a different theatre name");
      }
    },
    async theatreDetails() {
      const response = await fetch(
        `http://localhost:5000/api/theatre-details/${this.$route.params.theatre_id}`,
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

<style></style>
