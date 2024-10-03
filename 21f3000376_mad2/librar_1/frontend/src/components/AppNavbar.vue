<template>
  <nav>
    <div class="navbar-left">
      <router-link v-if="isAuthenticated && userRole === 'admin'" to="/admin-dashboard" class="logo-link">
        <img src="@/assets/logo.png" alt="Librar Logo" class="logo">
        <span class="app-name">Librar</span>
      </router-link>
      <router-link v-if="isAuthenticated && userRole === 'user'" to="/user-dashboard" class="logo-link">
        <img src="@/assets/logo.png" alt="Librar Logo" class="logo">
        <span class="app-name">Librar</span>
      </router-link>
      <div v-if="!isAuthenticated" class="logo-link">
        <img src="@/assets/logo.png" alt="Librar Logo" class="logo">
        <span class="app-name">Librar</span>
      </div>
    </div>
    <div class="navbar-links">
      <template v-if="isAuthenticated">
        <template v-if="userRole === 'admin'">
          <router-link to="/admin-dashboard">Home</router-link>
          <router-link to="/admin-requests">Requests</router-link>
          <router-link to="/admin-stats">Stats</router-link>
        </template>
        <template v-if="userRole === 'user'">
          <router-link to="/user-dashboard">Home</router-link>
          <router-link to="/user-books">Bag</router-link>
          <router-link to="/user-requests">Requests</router-link>
        </template>
        <button @click="logout" class="logout-button">Logout</button>
      </template>
      <template v-if='!isAuthenticated'>
        <router-link to="/login">Login</router-link>
        <router-link to="/signup">Signup</router-link>
      </template>
    </div>
  </nav>
</template>

<script>
import { mapGetters, mapActions } from 'vuex';

export default {
  name: 'AppNavbar',
  computed: {
    ...mapGetters(['isAuthenticated', 'userRole'])
  },
  methods: {
    ...mapActions(['logout'])
  }
};
</script>

<style>
nav {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px;
  background-color: #f8f9fa;
  border-bottom: 1px solid #e7e7e7;
}

.navbar-left {
  display: flex;
  align-items: center;
}
.logo{
  height: 70px;
  margin-right: 10px;
}
.logo-link {
  display: flex;
  align-items: center;
  text-decoration: none;
}



.app-name {
  font-size: 24px;
  font-weight: bold;
  color: #2c3e50;
  line-height: 60px
}

.navbar-links {
  display: flex;
  align-items: center;
}

.navbar-links a {
  margin-right: 15px;
  font-weight: bold;
  color: #2c3e50;
}

.navbar-links a.router-link-exact-active {
  color: #32a3e4;
}

.logout-button {
  background-color: #dc3545;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  font-weight: bold;
}

.logout-button:hover {
  background-color: #c82333;
}
</style>
