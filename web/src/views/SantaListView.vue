<template>
  <div class="santa-list-view">
    <b-card id="signup-form">
      <h4>Sign Up For Secret Santa</h4>
      <b-form @submit.prevent="onSubmit">
        <b-form-group label="Name" label-for="name">
          <b-form-input id="name" v-model="formName" required></b-form-input>
        </b-form-group>
        <b-form-group label="Email" label-for="email">
          <b-form-input id="email" v-model="formEmail" required></b-form-input>
        </b-form-group>
        <b-form-group label="Exclude from matching (Significant others)" label-for="exclude">
          <b-form-select id="exclude" v-model="formExclude" :options="participantNames"></b-form-select>
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
      <div v-if="listParticipants.length === 0">
        <p>No participants yet.</p>
      </div>
      <b-list-group>
        <b-list-group-item v-for="participant in listParticipants" :key="participant.name">
          <b>Name:</b> {{ participant.name }}<br>
          <b>Gift Ideas</b><br>
          <hr>
          <div v-for="line in participant.ideas.split('\n')" :key="line">{{ line }}</div>
        </b-list-group-item>
      </b-list-group>
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
      formEmail: '',
      formExclude: '',
      formIdeas: '',
      listUuid: '1234',
      listName: 'Santa List Name',
      listParticipants: [
        {
          name: 'Mitch',
          email: 'testemail123@example.com',
          ideas: 'blah blah blah\nblah blah'
        }
      ]
    }
  },
  computed: {
    participantNames () {
      if (this.listParticipants.length === 0) {
        return []
      }
      return this.listParticipants.map(participant => participant.name)
    }
  },
  methods: {
    onSubmit (event) {
      event.preventDefault()
      this.$http.post('https://santa-api.mitchmcaffee.com/list/' + this.listUuid + '/participant', {
        name: this.formName,
        email: this.formEmail,
        exclude: this.formExclude,
        ideas: this.formIdeas
      }).then(response => {
        this.getList()
        this.resetForm()
      }, response => {
        console.log(response)
      })
    },
    getList () {
      this.listUuid = this.$route.params.id
      console.log(this.listUuid)
      this.$http.get('https://santa-api.mitchmcaffee.com/list/' + this.listUuid).then(response => {
        this.listName = response.data.list.name
        this.listParticipants = response.data.list.participants
      }, response => {
        console.log(response)
      })
    },
    resetForm () {
      this.formName = ''
      this.formEmail = ''
      this.formExclude = ''
      this.formIdeas = ''
    }
  }
}
</script>
