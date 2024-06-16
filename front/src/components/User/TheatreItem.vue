<template>
  <div class="theatre-item m-1">
    <div class="name">
      <h3>{{ tname }}</h3>
    </div>
    <p>{{ place }}</p>
    <router-link
      class="btn btn-sm btn-danger"
      :to="{
        name: 'TheatreDetails',
        params: {
          theatre_id: id,
        },
      }"
    >
      Shows ->
    </router-link>
  </div>
</template>

<script>
export default {
  name: "TheatreItem",
  props: ["tname", "place", "id"],
};
</script>

<style>
.theatre-item {
  box-shadow: rgba(0, 0, 0, 0.16) 0px 1px 4px;
  padding: 10px;
  width: 32%;
}
</style>
