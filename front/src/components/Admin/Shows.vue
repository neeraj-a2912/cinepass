<template>
  <div class="container my-0">
    <AdminNavbar />
    <div class="downloa">
      <button @click.prevent="downloadShows" class="btn btn-sm btn-secondary">Download Shows</button>
    </div>
    <div class="theatre-list">
      <table class="table mt-3 table-borderless">
        <thead>
          <tr class="table-dark">
            <th scope="col">Name</th>
            <th scope="col">Tags</th>
            <th scope="col">Capacity</th>
            <th scope="col">Ticket Price</th>
            <th scope="col">Date</th>
            <th scope="col">Screen</th>
            <th scope="col">Update</th>
            <th scope="col">Delete</th>
            <th scope="col">Export</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="show in shows" :key="show.id">
            <td>
              {{ show.name }}
            </td>
            <td>{{ show.tags }}</td>
            <td>{{ show.capacity }}</td>
            <td>{{ show.ticket_price }}</td>
            <td>{{ show.show_date }}</td>
            <td>{{ show.screen_number }}</td>
            <td>
              <router-link
                class="btn btn-secondary btn-sm"
                :to="{
                  name: 'UpdateShow',
                  params: {
                    show_id: show.id,
                  },
                }"
                >Update</router-link
              >
            </td>
            <td>
              <button
                class="btn btn-sm btn-danger"
                @click="confirmDelete(show.id)"
              >
                Delete
              </button>
            </td>
            <td
              class="material-symbols-outlined"
              @click="handleExport(show.id)"
              style="cursor: pointer"
            >
              ios_share
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import AdminNavbar from "./AdminNavbar.vue";
export default {
  name: "AdminShows",
  components: { AdminNavbar },
  data() {
    return {
      shows: [],
    };
  },
  mounted() {
    this.getShowList();
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
        console.log(this.shows);
      }
    },
    async deleteShow(show_id) {
      const response = await fetch(
        `http://localhost:5000/api/show/${this.$route.params.theatre_id}/${show_id}`,
        {
          method: "DELETE",
          headers: {
            "Content-Type": "application/json",
            Authorization: "Bearer " + localStorage.getItem("access-token"),
          },
        }
      );
      if (response.ok) {
        this.shows = this.shows.filter((show) => show.id !== show_id);
        alert("Show Deleted Successfully");
      }
    },
    confirmDelete(show_id) {
      if (confirm("Are you sure you want to delete this show?")) {
        this.deleteShow(show_id);
      }
    },
    async handleExport(show_id) {
      const response = await fetch(
        `http://localhost:5000/api/export/show/${show_id}`,
        {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            Authorization: "Bearer " + localStorage.getItem("access-token"),
          },
        }
      );
      if (response.ok) {
        const data = await response.json;
        console.log(data);
        alert("mail sent");
      }
    },
    downloadShows() {
      let csv =
        "Name,tags,capacity,ticket_price,date,screen_number,theatre,place\n";

      this.shows.forEach((show) => {
        let li = [];
        li.push(show.name);
        li.push(show.tags);
        li.push(show.capacity);
        li.push(show.ticket_price);
        li.push(show.show_date);
        li.push(show.screen_number)
        li.push(show.theatre)
        li.push(show.place)
        csv += li.join(",");
        csv += "\n";
      });

      const anchor = document.createElement("a");
      anchor.href = "data:text/csv;charset=utf-8," + encodeURIComponent(csv);
      anchor.target = "_blank";
      anchor.download = `theatre_${this.$route.params.theatre_id}.csv`;
      anchor.click();
    },
  },
};
</script>

<style scoped></style>
