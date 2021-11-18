<template>
  <div id="app">
    <div class="container">
      <router-view/>
    </div>
  </div>
</template>

<style>
body {
  background-image: url('~@/assets/knit.jpg');
  background-repeat: repeat-x repeat-y;
}
#app {
  padding-top: 2em;
  padding-bottom: 2em;
}

#nav {
  padding: 30px;
}

#nav a {
  font-weight: bold;
  color: #2c3e50;
}

#nav a.router-link-exact-active {
  color: #42b983;
}
</style>
