<template>
  <div class="container">
    <NavbarHome />
    <form @submit.prevent="registerUser">
      <label for="name" class="form-label">UserName</label><br />
      <input
        type="text"
        class="form-control shadow-none"
        name="name"
        v-model="formData.name"
        required
      /><br />
      <label for="email" class="form-label">Email Address</label><br />
      <input
        type="email"
        class="form-control shadow-none"
        name="email"
        v-model="formData.email"
        required
      /><br />
      <label for="password" class="form-label">Password</label><br />
      <input
        type="password"
        class="form-control shadow-none"
        name="password"
        v-model="formData.password"
        required
      /><br />
      <label for="role" class="form-label">Select Role</label>
      <select
        name="role"
        class="form-select shadow-none"
        v-model="formData.role"
      >
        <option value="admin">Admin</option>
        <option value="user" selected>User</option></select
      ><br />
      <div v-if="isLoading">
        <SpinnerItem/>
      </div>
      <button class="btn btn-danger">Register</button><br />
      <p class="my-2" style="text-align: center">
        Already Have an Account?
        <router-link
          class="btn btn-sm btn-secondary"
          :to="{ name: 'UserLogin' }"
          >Login</router-link
        >
      </p>
    </form>
  </div>
</template>

<script>
import NavbarHome from "./NavbarHome.vue";
import SpinnerItem from "./Spinner.vue"
export default {
  name: "RegisterForm",
  components: { NavbarHome, SpinnerItem },
  data() {
    return {
      formData: {
        name: "",
        email: "",
        password: "",
        role: "",
      },
      isLoading: false,
    };
  },
  methods: {
    async registerUser() {
      const response = await fetch("http://localhost:5000/api/user", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(this.formData),
      });
      const data = response.json();
      console.log(data);
      if (response.ok) {
        this.$router.push({ name: "UserLogin" });
      }
    },
  },
};
</script>
