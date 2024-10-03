<template>
  <div class="login-container">
    <h2>Login</h2>
    <form @submit.prevent="loginUser" class="form-container">
      <div class="form-group">
        <label for="username">Username:</label>
        <input type="text" id="username" v-model="username" required />
      </div>
      <div class="form-group">
        <label for="password">Password:</label>
        <input type="password" id="password" v-model="password" required />
      </div>
      <button type="submit" class="login-button">Login</button>
    </form>
    <div v-if="errorMessage" class="error-message">
      {{ errorMessage }}
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      username: '',
      password: '',
      errorMessage: ''
    };
  },
  methods: {
    async loginUser() {
      try {
        const response = await axios.post('http://127.0.0.1:5000/api/login', {
          username: this.username,
          password: this.password
        });
        const { access_token, user } = response.data;
        localStorage.setItem('user', JSON.stringify(user));

        // Update Vuex store
        this.$store.dispatch('login', { token: access_token, user });

        // Navigate based on user role
        if (user.role === 'admin') {
          this.$router.push('/admin-dashboard');
        } else {
          this.$router.push('/user-dashboard');
        }
      } catch (error) {
        this.errorMessage = error.response ? error.response.data.message : 'Invalid Username or Password';
      }
    }
  }
};
</script>

<style>
.login-container {
  max-width: 400px;
  margin: 50px auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 8px;
  background-color: #f9f9f9;
}

h2 {
  text-align: center;
  margin-bottom: 20px;
}

.form-container {
  display: flex;
  flex-direction: column;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

.form-group input {
  width: 100%;
  padding: 8px;
  box-sizing: border-box;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.login-button {
  padding: 10px;
  background-color: #32a3e4;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
  text-align: center;
}

.login-button:hover {
  background-color: #258bb5;
}

.error-message {
  color: red;
  text-align: center;
  margin-top: 10px;
}
</style>
