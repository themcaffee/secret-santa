<template>
  <div class="santa-list-view">
    <b-card class="card-margin">
      <h4>Sign Up For Secret Santa</h4>
      <b-form @submit.prevent="onSubmit">
        <b-form-group label="Name" label-for="name">
          <b-form-input id="name" v-model="formName" required></b-form-input>
        </b-form-group>
        <b-form-group label="Email" label-for="email">
          <b-form-input id="email" v-model="formEmail" required></b-form-input>
        </b-form-group>
        <b-form-group label="Exclude from matching like Significant others (Optional)" label-for="exclude">
          <b-form-select id="exclude" v-model="formExclude" :options="participantNames"></b-form-select>
        </b-form-group>
        <b-form-group label="Gift ideas & Interests" label-for="ideas">
          <b-form-textarea
            id="ideas"
            v-model="formIdeas"
            placeholder="Write something good! You will not be able to change this later."
            rows="8"></b-form-textarea>
        </b-form-group>
        <br>
        <b-button block type="submit" variant="primary">Submit</b-button>
      </b-form>
    </b-card>
    <b-card class="card-margin">
      <b-input-group>
        <b-form-input id="password" v-model="formPassword" placeholder="List Creator Password" type="password"></b-form-input>
        <b-input-group-append>
          <b-button variant="primary" @click="sendEmails()">Pair & Send Emails</b-button>
        </b-input-group-append>
      </b-input-group>
    </b-card>
    <b-card class="card-margin">
      <h3>{{ listName }}</h3>
      <div v-if="listParticipants.length === 0">
        <p>No participants yet.</p>
      </div>
      <b-list-group>
        <b-list-group-item v-for="participant in listParticipants" :key="participant.name">
          <b>Name:</b> {{ participant.name }}<br>
          <b>Gift Ideas:</b><br>
          <div v-for="line in participant.ideas.split('\n')" :key="line">{{ line }}</div>
        </b-list-group-item>
      </b-list-group>
    </b-card>
  </div>
</template>

<style scoped>
.card-margin {
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
      formPassword: '',
      listUuid: '',
      listName: '',
      listParticipants: []
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
    /*
      Add a participant to this list
    */
    onSubmit (event) {
      event.preventDefault()
      this.$http.post('https://santa-api.mitchmcaffee.com/list/' + this.listUuid + '/participant', {
        name: this.formName,
        email: this.formEmail,
        exclude: this.formExclude,
        ideas: this.formIdeas
      }).then(response => {
        this.$bvToast.toast('Participant added!')
        this.getList()
        this.resetForm()
      }, response => {
        this.$bvToast.toast('Error submitting form')
        console.error(response)
      })
    },
    /*
      Get the list defined in the URL from vue-router
    */
    getList () {
      this.listUuid = this.$route.params.id
      this.$http.get('https://santa-api.mitchmcaffee.com/list/' + this.listUuid).then(response => {
        this.listName = response.data.list.name
        this.listParticipants = response.data.list.participants
      }, response => {
        this.$bvToast.toast('Error getting list')
        console.error(response)
      })
    },
    resetForm () {
      this.formName = ''
      this.formEmail = ''
      this.formExclude = ''
      this.formIdeas = ''
      this.formPassword = ''
    },
    sendEmails () {
      this.$http.post('https://santa-api.mitchmcaffee.com/list/' + this.listUuid + '/send', {
        password: this.formPassword
      }).then(response => {
        this.$bvToast.toast('Sent emails successfully')
        this.getList()
        this.resetForm()
      }, response => {
        this.$bvToast.toast('Error sending emails')
        console.error(response)
      })
    }
  }
}
</script>
