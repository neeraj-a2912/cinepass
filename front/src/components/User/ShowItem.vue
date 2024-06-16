<template>
  <div class="show-item">
    <div class="top">
        <h4>{{ name }}</h4>
        <div class="date-time">
          <p class="mx-2">{{ show_date }}</p>
          <p><b>{{ timing }}</b></p>
        </div>
    </div>
    <p class="m-0">Screen {{ screen }}, {{ theatre }}, {{ place }}</p>
    <p class="m-0">Ratings: {{ ratings }}/5 </p>
    <p class="m-0">{{ tags }}</p>
    <div class="bottom">
      <p class="m-0">Available Seats - {{ capacity }}</p>
      <p class="m-0"><b>Rs. {{ ticket_price }}</b></p>
    </div>
    <router-link v-if="capacity>0"
      class="btn btn-danger btn-sm mt-3"
      :to="{ name: 'BookingItem', params: { show_id: id } }"
      >Book Tickets</router-link
    >
    <p v-else class="btn btn-danger btn-sm mt-3 mb-0 disabled">HouseFull</p>
  </div>
</template>

<script>
export default {
  name: "ShowItem",
  props: ["name", "tags", "ticket_price", "ratings", "id", "capacity", "timing", "show_date", "theatre", "place", "screen"],
  data() {
    return {
      user: localStorage.getItem("role"),
    };
  },
  methods: {
    async deleteShow(show_id) {
      const response = await fetch(
        `http://localhost:5000/api/show/${this.$route.params.theatre_id}/${show_id}`,
        {
          method: "DELETE",
          headers: {
            "Content-Type": "application/json",
            // "Access-Control-Allow-Origin": "*",
            Authorization: "Bearer " + localStorage.getItem("access-token"),
          },
        }
      );
      if (response.ok) {
        alert("Show Deleted Successfully");
        this.$router.push({
          name: "AdminDashBoard",
        });
      }
    },
  },
};
</script>

<style>
.show-item {
  box-shadow: rgba(0, 0, 0, 0.16) 0px 1px 4px;
  padding: 13px;
  margin: 2px 0;
  width: 49%;
  margin: 4px auto;
}
.show-item .top, .bottom{
  display: flex;
  justify-content: space-between;
}

.show-item .top .name{
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.show-item .top .date-time{
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
