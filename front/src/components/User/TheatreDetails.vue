<template>
  <div class="container">
    <UserNavbar />
    <div class="show-items">
      <ShowItem
        v-for="show in shows"
        :key="show.id"
        :name="show.name"
        :tags="show.tags"
        :ticket_price="show.ticket_price"
        :id="show.id"
        :ratings="show.ratings"
        :capacity="show.capacity"
        :timing="show.show_timing"
        :show_date="show.show_date"
        :place="show.place"
        :screen="show.screen_number"
        :theatre="show.theatre"
      />
    </div>
  </div>
</template>

<script>
import ShowItem from "./ShowItem.vue";
import UserNavbar from "./UserNavbar.vue";
export default {
  name: "TheatreDetails",
  components: { ShowItem, UserNavbar },
  data() {
    return {
      shows: [],
      role: localStorage.getItem("role"),
    };
  },
  mounted() {
    if (this.shows.length === 0) {
      this.getShowList();
    }
  },
  methods: {
    async getShowList() {
      const response = await fetch(
        `http://localhost:5000/api/show/${this.$route.params.theatre_id}`,
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
        this.shows = data;
        console.log(this.shows)
      }
    },
  },
};
</script>

<style>
.show-items{
  display: flex;
  flex-wrap: wrap;
}
</style>