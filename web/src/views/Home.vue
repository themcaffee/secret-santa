<template>
  <div class="home">
    <b-card>
      <h1>Secret Santa List Creator</h1>
      <p>This is a tool created for friends and family to create secret santa lists, have people join them, and send
      out emails to participants. Your email address will never be used for any purposes other than receiving your secret santa.
      This project is open source, <a href="https://github.com/themcaffee/secret-santa">check me out.</a></p>
    </b-card>
    <b-card>
      <h3>Create New Secret Santa List</h3>
      <b-form @submit.prevent="onSubmit">
        <b-form-group label="Group Name" label-for="name">
          <b-form-input id="name" v-model="formName" required></b-form-input>
        </b-form-group>
        <b-form-group label="Password (for sending out emails)" label-for="password">
          <b-form-input id="password" type="password" v-model="formPassword" required></b-form-input>
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
      formName: '',
      formPassword: ''
    }
  },
  methods: {
    /*
      Create a new santa list
    */
    onSubmit (event) {
      event.preventDefault()
      this.$http.post('https://santa-api.mitchmcaffee.com/list', {
        name: this.formName,
        password: this.formPassword
      }).then(response => {
        this.$router.push({ name: 'SantaListView', params: { id: response.body.list.uuid } })
      }, response => {
        console.error(response)
      })
    }
  }
}
</script>
