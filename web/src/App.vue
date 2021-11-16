<template>
  <div id="app">
    <!--
    <div id="nav">
      <router-link to="/">Home</router-link>
    </div>
    -->
    <div class="container">
      <router-view/>
    </div>
  </div>
</template>

<style>
#app {
  padding-top: 2em;
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
