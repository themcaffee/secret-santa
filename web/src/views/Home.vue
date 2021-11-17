<template>
  <div class="home">
    <b-card>
      <h3>Create New Secret Santa List</h3>
      <b-form @submit="onSubmit">
        <b-form-group label="Group Name" label-for="name">
          <b-form-input id="name" v-model="name" required></b-form-input>
        </b-form-group>
        <b-form-group label="Password (for sending out emails)" label-for="password">
          <b-form-input id="password" type="password" v-model="formName" required></b-form-input>
        </b-form-group>
        <br>
        <b-button block type="submit" variant="primary">Submit</b-button>
      </b-form>
    </b-card>
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
