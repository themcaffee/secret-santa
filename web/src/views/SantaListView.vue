<template>
  <div class="santa-list-view">
    <b-card id="signup-form">
      <h4>Sign Up For Secret Santa</h4>
      <b-form @submit="onSubmit">
        <b-form-group label="Name" label-for="name">
          <b-form-input id="name" v-model="formName" required></b-form-input>
        </b-form-group>
        <b-form-group label="Gift ideas & Interests" label-for="ideas">
          <b-form-textarea
            id="ideas"
            placeholder="Write something good! You will not be able to change this later."
            rows="8"></b-form-textarea>
        </b-form-group>
        <br>
        <b-button block type="submit" variant="primary">Submit</b-button>
      </b-form>
    </b-card>
    <b-card>
      <h3>{{ listName }}</h3>
      <ul>
        <li v-for="participant in listParticipants" :key="participant.name">
          {{ participant.name }}
        </li>
      </ul>
    </b-card>
  </div>
</template>

<style scoped>
#signup-form {
  margin-bottom: 2em;
}
</style>

<script>
export default {
  name: 'SantaListView',
  mounted () {
    this.getList()
  },
  data () {
    return {
      formName: '',
      listUuid: '1234',
      listName: 'Santa List',
      listParticipants: [
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
    },
    getList () {
      this.listUuid = this.$route.params.id
      console.log(this.listUuid)
      this.$http.get('https://santa-api.mitchmcaffee.com/list/' + this.listUuid).then(response => {
        this.listName = response.data.name
        this.listParticipants = response.data.participants
      }, response => {
        console.log(response)
      })
    }
  }
}
</script>
