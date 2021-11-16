<template>
  <div class="home">
    <h3>Create New Secret Santa List</h3>
    <b-form @submit="onSubmit">
      <b-form-group label="Group Name" label-for="name">
        <b-form-input id="name" v-model="name" required></b-form-input>
      </b-form-group>
      <b-button type="submit" variant="primary">Submit</b-button>
    </b-form>
  </div>
</template>

<script>

export default {
  name: 'Home',
  data () {
    return {
      name: ''
    }
  },
  onSubmit (event) {
    event.preventDefault()
  }
}
</script>
