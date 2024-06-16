<template>
  <div class="container">
    <UserNavbar />
    <form @submit.prevent="search">
      <input
        name="searchItem"
        class="form-control shadow-none"
        placeholder="Search a Show or Theatre"
        v-model="toBeSearched"
      />
      <button class="btn btn-sm btn-secondary mt-2">Search</button>
    </form>
    <div class="search-result mx-auto m-0">
      <div class="shows" v-if="shows.length !== 0">
        <div class="show-items" v-for="show in shows" :key="show.id">
          <router-link
            style="color: black"
            :to="{ name: 'BookingItem', params: { show_id: show.id } }"
            ><h6 class="m-0">
              <b>{{ show.name }}</b>
            </h6>
            <p class="m-0" style="font-size: 11px">
              {{ show.theatre }}, {{ show.location }}
            </p>
          </router-link>
        </div>
      </div>
      <div class="theatres" v-if="theatres.length != 0">
        <div
          class="theatre-items"
          v-for="theatre in theatres"
          :key="theatre.id"
        >
          <router-link
            style="color: black"
            :to="{
              name: 'TheatreDetails',
              params: {
                theatre_id: theatre.id,
              },
            }"
          >
            <p class="m-0">
              <b>{{ theatre.name }}</b
              >, <span style="font-size: 12px">{{ theatre.place }}</span>
            </p>
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import UserNavbar from "./UserNavbar.vue";
export default {
  name: "SearchBar",
  components: { UserNavbar },
  data() {
    return {
      shows: [],
      theatres: [],
      toBeSearched: "",
    };
  },
  mounted() {},
  methods: {
    async search() {
      const response = await fetch(
        `http://localhost:5000/api/search/${this.toBeSearched}`,
        {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            Authorization: "Bearer " + localStorage.getItem("access-token"),
          },
        }
      );
      console.log(response);
      if (response.ok) {
        const data = await response.json();
        this.shows = data.shows;
        this.theatres = data.theatres;
      }
    },
  },
};
</script>

<style scoped>
.search-result {
  width: 50%;
  padding: 10px;
}

.theatre-items,
.show-items {
  box-shadow: rgba(0, 0, 0, 0.16) 0px 1px 4px;
  padding: 10px;
  margin: 3px;
}
</style>
