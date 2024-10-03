<template>
  <div class="signup-container">
    <h2>Signup</h2>
    <form @submit.prevent="signupUser" class="form-container">
      <div class="form-group">
        <label for="username">Username:</label>
        <input type="text" id="username" v-model="username" required />
      </div>
      <div class="form-group">
        <label for="email">Email:</label>
        <input type="email" id="email" v-model="email" required />
      </div>
      <div class="form-group">
        <label for="password">Password:</label>
        <input type="password" id="password" v-model="password" required />
      </div>
      <button type="submit" class="signup-button">Signup</button>
    </form>
    <div v-if="errorMessage" class="error-message">
      {{ errorMessage }}
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { useToast } from 'vue-toastification';

export default {
  data() {
    return {
      username: '',
      email: '',
      password: '',
      errorMessage: '',
    };
  },
  methods: {
    async signupUser() {
      const toast = useToast();
      try {
        await axios.post('http://127.0.0.1:5000/api/signup', {
          username: this.username,
          email: this.email,
          password: this.password,
        });
        toast.success('Signup successful!');
        this.$router.push('/login'); // Redirect to login page after signup
      } catch (error) {
        this.errorMessage = error.response ? error.response.data.message : 'Signup failed. Please try again';
      }
    }
  }
};
</script>

<style>
.signup-container {
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

.signup-button {
  padding: 10px;
  background-color: #32a3e4;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
  text-align: center;
}

.signup-button:hover {
  background-color: #258bb5;
}

.error-message {
  color: red;
  text-align: center;
  margin-top: 10px;
}
</style>
