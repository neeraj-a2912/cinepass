<template>
  <div class="container my-0">
    <AdminNavbar />
    <form @submit.prevent="addTheatre" action="">
      <h3>Add New Theatre</h3>
      <label for="name">Name</label><br />
      <input
        type="text"
        name="name"
        v-model="formData.name"
        class="form-control form-control-sm shadow-none"
        required
      /><br />
      <label for="place">Place</label><br />
      <input
        type="text"
        name="place"
        class="form-control form-control-sm shadow-none"
        v-model="formData.place"
        required
      /><br />
      <label for="screens">Screens</label><br />
      <input
        type="number"
        name="screens"
        min="1"
        required
        class="form-control form-control-sm shadow-none"
        v-model="formData.screens"
      /><br/>
      <button class="btn btn-secondary">Add Theatre</button>
    </form>
  </div>
</template>

<script>
import AdminNavbar from "./AdminNavbar.vue";
export default {
  name: "AddTheatre",
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
  methods: {
    async addTheatre() {
      console.log("add theatre clicked");
      const response = await fetch("http://localhost:5000/api/theatre", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: "Bearer " + localStorage.getItem("access-token"),
        },
        body: JSON.stringify(this.formData),
      });
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
  },
};
</script>

<style></style>
