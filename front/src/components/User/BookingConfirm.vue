<template>
  <div class="container">
    <UserNavbar />
    <div class="confirm">
      <img
        src="../../assets/bookingConfirm.jpg"
        class="mx-auto"
        alt="Booking Confirmed"
      />
      <p>
        Your Booking is Confirmed. The Ticket will be Available in
        <b>'My Bookings'</b> Section.
      </p>
    </div>
  </div>
</template>

<script>
import UserNavbar from "./UserNavbar.vue";
export default {
  name: "BookingConfirm",
  components: { UserNavbar },
};
</script>

<style scoped>
.confirm {
  width: 100%;
  margin: auto;
  text-align: center;
}
img {
  width: 70%;
  height: 500px;
  align-items: center;
}
p {
  color: rgb(4, 175, 4);
  font-size: 20px;
}
</style>
