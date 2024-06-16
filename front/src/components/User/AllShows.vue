<template>
  <div class="container">
    <UserNavbar />
    <div class="d-flex">
      <div class="date">
        <label for="show_date">Search By Date</label>
        <input
          type="date"
          class="form-control form-control-sm shadow-none"
          name="show_date"
          v-model="date"
          @change="filteredShows()"
          required
        />
      </div>
      <div class="rating mx-5">
        <label for="rating">Rating</label>
        <input
          type="number"
          class="form-control form-control-sm shadow-none"
          name="rating"
          v-model="rating"
          @change="filteredShows()"
          min="0"
          max="5"
          required
        />
        <br />
      </div>
    </div>
    <div class="filtered show-items">
      <ShowItem
        v-for="show in filtered"
        :key="show.id"
        :name="show.name"
        :tags="show.tags"
        :ticket_price="show.ticket_price"
        :id="show.id"
        :ratings="show.ratings"
        :capacity="show.capacity"
        :timing="show.show_timing"
        :show_date="show.show_date"
        :theatre="show.theatre"
        :place="show.place"
        :screen="show.screen_number"
      />
    </div>
  </div>
</template>

<script>
import ShowItem from "./ShowItem.vue";
import UserNavbar from "./UserNavbar.vue";
export default {
  name: "AllShows",
  components: { ShowItem, UserNavbar },
  data() {
    return {
      shows: [],
      filtered: [],
      role: localStorage.getItem("role"),
      date: "",
      rating: null,
    };
  },
  mounted() {
    this.getAllShows();
  },
  methods: {
    async getAllShows() {
      const response = await fetch("http://localhost:5000/api/get-all-shows", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          "Access-Control-Allow-Origin": "*",
          Authorization: "Bearer " + localStorage.getItem("access-token"),
        },
      });
      const data = await response.json();
      if (response.ok) {
        this.shows = data;
        this.filtered = data;
        console.log("filtered", this.filtered);
      }
    },
    filteredShows() {
      if (this.date && this.rating) {
        this.filtered = this.shows.filter(
          (show) =>
            show.show_date === this.date && show.ratings === this.rating
        );
      } else if (this.rating) {
        this.filtered = this.shows.filter(
          (show) => show.ratings === this.rating
        );
      } else if (this.date) {
        this.filtered = this.shows.filter(
          (show) => show.show_date === this.date
        );
      } else {
        this.filtered = this.shows;
      }
    },
  },
};
</script>
