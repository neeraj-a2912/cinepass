<template>
  <div class="container">
    <NavbarHome />
    <form @submit.prevent="loginUser">
      <h1>User Login</h1>
      <label for="email" class="form-label form-label-sm">Email</label><br />
      <input
        type="email"
        name="email"
        class="form-control form-control-sm shadow-none"
        v-model="email"
        required
      /><br />
      <label for="password" class="form-label form-label-sm">Password</label
      ><br />
      <input
        type="password"
        name="password"
        class="form-control form-control-sm shadow-none"
        v-model="password"
        required
      /><br />
      <p style="color: red; text-align: center" v-if="message">{{ message }}</p>
      <div v-if="isLoading">
        <SpinnerItem />
      </div>
      <button class="btn btn-danger">Login</button><br />
      <p style="text-align: center" class="my-3">
        Don't Have an Account?
        <router-link
          class="btn btn-sm btn-secondary"
          :to="{ name: 'RegisterForm' }"
          >Register</router-link
        >
      </p>
    </form>
  </div>
</template>

<script>
import NavbarHome from "../NavbarHome.vue";
import SpinnerItem from "../Spinner.vue";
export default {
  name: "UserLogin",
  components: { NavbarHome, SpinnerItem },
  data() {
    return {
      email: "",
      password: "",
      message: null,
      isLoading: false,
    };
  },
  methods: {
    async loginUser() {
      this.isLoading = true;
      const response = await fetch("http://localhost:5000/api/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email: this.email,
          password: this.password,
        }),
      });
      const data = await response.json();
      if (!data.status) {
        this.isLoading = false;
        if (data.user) {
          this.message = "User Not Found";
        } else {
          this.message = "Incorrect Password";
        }
        return;
      }
      if (response.ok) {
        this.isLoading = false;
        localStorage.setItem("access-token", data.access_token);
        localStorage.setItem("user_id", data.user_id);
        localStorage.setItem("role", data.role);
        localStorage.setItem("name", data.name);
        if (data.role === "admin") {
          return this.$router.push({ name: "AdminDashBoard" });
        }
        return this.$router.push({ name: "UserDashBoard" });
      } else {
        this.isLoading = false;
        console.log("error");
      }
    },
  },
};
</script>
