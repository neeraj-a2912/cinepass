<template>
  <div class="container my-0">
    <AdminNavbar />
    <div class="add-export">
      <router-link
        class="btn btn-sm btn-secondary"
        :to="{ name: 'AddTheatre' }"
      >
        Add New Theatre</router-link
      >
      <div class="download-export">
        <p
          @click.prevent="downloadTheatres"
          class="material-symbols-outlined mx-3"
          style="cursor: pointer;"
        >
          download
        </p>
        <p
          class="m-0 material-symbols-outlined"
          @click.prevent="handleExport(0)"
          style="cursor: pointer"
        >
          ios_share
        </p>
      </div>
    </div>

    <div class="theatre-list">
      <table class="table mt-3 table-borderless">
        <thead>
          <tr class="table-dark">
            <th scope="col">Theatre Name</th>
            <th scope="col">Place</th>
            <th scope="col">Screens Available</th>
            <th scope="col">Add Show</th>
            <th scope="col">Update</th>
            <th scope="col">Delete</th>
            <th scope="col">Export</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="theatre in theatres" :key="theatre.id">
            <td>
              <router-link
                style="color: black"
                :to="{
                  name: 'AdminShows',
                  params: {
                    theatre_id: theatre.id,
                  },
                }"
                >{{ theatre.name }}</router-link
              >
            </td>
            <td>{{ theatre.place }}</td>
            <td>{{ theatre.screens }}</td>
            <td>
              <div v-if="theatre.screens === 0" class="screens-full">
                <button class="btn btn-secondary btn-sm disabled">
                  Screens Full
                </button>
              </div>
              <div v-else>
                <router-link
                  class="btn btn-secondary btn-sm"
                  :to="{
                    name: 'AddShow',
                    params: { theatre_id: theatre.id },
                  }"
                  >Add New Show</router-link
                >
              </div>
            </td>
            <td>
              <router-link
                class="btn btn-secondary btn-sm"
                :to="{
                  name: 'UpdateTheatre',
                  params: {
                    theatre_id: theatre.id,
                  },
                }"
                >Update</router-link
              >
            </td>
            <td>
              <button
                class="btn btn-sm btn-danger"
                @click="confirmDelete(theatre.id)"
              >
                Delete
              </button>
            </td>
            <td
              class="material-symbols-outlined"
              @click="handleExport(theatre.id)"
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
  name: "AdminDashBoard",
  components: { AdminNavbar },
  data() {
    return {
      theatres: [],
      downloadlink: null,
      currentTheatre: null,
    };
  },
  mounted() {
    this.getTheatreList();
  },
  methods: {
    async getTheatreList() {
      const response = await fetch("http://localhost:5000/api/theatre", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          "Access-Control-Allow-Origin": "*",
          Authorization: "Bearer " + localStorage.getItem("access-token"),
        },
      });
      const data = await response.json();
      if (response.ok) {
        this.theatres = data;
        console.log(this.theatres);
      }
    },
    async deleteTheatre(theatre_id) {
      const response = await fetch(
        `http://localhost:5000/api/theatre/${theatre_id}`,
        {
          method: "DELETE",
          headers: {
            "Content-Type": "application/json",
            Authorization: "Bearer " + localStorage.getItem("access-token"),
          },
        }
      );
      if (response.ok) {
        this.theatres = this.theatres.filter(
          (theatre) => theatre.id !== theatre_id
        );
        alert("Theatre Deleted Successfully");
      }
    },
    confirmDelete(theatre_id) {
      if (confirm("Are you sure you want to delete this theatre?")) {
        this.deleteTheatre(theatre_id);
      }
    },
    async handleExport(theatre_id) {
      const response = await fetch(
        `http://localhost:5000/api/export/theatre/${theatre_id}`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            Authorization: "Bearer " + localStorage.getItem("access-token"),
          },
        }
      );
      if (response.ok) {
        const data = await response.json();
        console.log(data);
        alert("mail sent");
      }
    },
    downloadTheatres() {
      let csv =
        "Theatre id, Theatre Name, Theatre Location, Screens Available, No of shows Currently Running\n";

      this.theatres.forEach((theatre) => {
        let li = [];
        li.push(theatre.id);
        li.push(theatre.name);
        li.push(theatre.place);
        li.push(theatre.screens);
        li.push(theatre.shows);
        csv += li.join(",");
        csv += "\n";
      });

      const anchor = document.createElement("a");
      anchor.href = "data:text/csv;charset=utf-8," + encodeURIComponent(csv);
      anchor.target = "_blank";
      anchor.download = "AllTheatresList.csv";
      anchor.click();
    },
  },
};
</script>

<style>
.add-export {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
