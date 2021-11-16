<template>
  <div class="santa-list-view">
    <h3>{{ name }}</h3>
    <hr>
    <h4>Sign Up</h4>
    <b-form @submit="onSubmit">
      <b-form-group label="Name" label-for="name">
        <b-form-input id="name" v-model="name" required></b-form-input>
      </b-form-group>
      <b-button type="submit" variant="primary">Submit</b-button>
    </b-form>
    <hr>
    <h4>Current List</h4>
    <ul>
      <li v-for="participant in participants" :key="participant.name">
        {{ person.name }}
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  name: 'SantaListView',
  data () {
    return {
      name: 'Santa List',
      participants: [
        {
          name: 'Mitch',
          email: 'testemail123@example.com'
        }
      ]
    }
  },
  methods: {
    onSubmit (event) {
      event.preventDefault()
    }
  }
}
</script>
