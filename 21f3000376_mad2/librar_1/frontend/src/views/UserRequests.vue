<template>
  <div class="user-requests">
    <h2>Book Requests</h2>
    <table v-if="requests.length > 0" class="request-table">
      <thead>
        <tr>
          <th>Book Name</th>
          <th>Author</th>
          <th>Date Created</th>
          <th>Return Date</th>
          <th>Status</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="request in requests" :key="request.id">
          <td>{{ request.book_name }}</td>
          <td>{{ request.book_author }}</td>
          <td>{{ request.issue_date }}</td>
          <td>{{ request.return_date }}</td>
          <td>{{ request.status }}</td>
          <td>
            <button @click="cancelRequest(request.id)" v-if="request.status === 'pending'" class="cancel-button">Cancel</button>
          </td>
        </tr>
      </tbody>
    </table>
    <div v-else>
      <p>No book requests found</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { mapGetters } from 'vuex';

export default {
  data() {
    return {
      requests: [],
      user_id: JSON.parse(localStorage.getItem('user')).id
    };
  },
  computed: {
    ...mapGetters(['user'])
  },
  created() {
    this.loadRequests();
  },
  methods: {
    async loadRequests() {
      try {
        const response = await axios.get(`http://127.0.0.1:5000/api/request/user/${this.user_id}`);
        this.requests = response.data.map(request => ({
          ...request,
          issue_date: request.issue_date || 'N/A',
          return_date: request.return_date || 'N/A'
        }));
      } catch (error) {
        console.error(error);
      }
    },
    async cancelRequest(requestId) {
      try {
        const response = await axios.delete(`http://127.0.0.1:5000/api/request/${requestId}`);
        console.log(response.data);
        this.loadRequests();
      } catch (error) {
        console.error(error);
      }
    },
    async addToRequestList(bookId) {
      try {
        const existingRequest = this.requests.find(request => request.book_id === bookId && ['pending', 'accepted'].includes(request.status));
        if (existingRequest) {
          console.error('You have already requested this book or the request is still pending.');
          return;
        }

        // Check if the user has 5 or more books accepted or pending
        const activeRequestsCount = this.requests.filter(request => ['pending', 'accepted'].includes(request.status)).length;
        if (activeRequestsCount >= 5) {
          console.error('You cannot request more than 5 books at a time. Please return some books first.');
          return;
        }

        const response = await axios.post('http://127.0.0.1:5000/api/request', {
          user_id: this.user_id,
          book_id: bookId
        });
        console.log(response.data);
        this.loadRequests();
      } catch (error) {
        console.error(error);
      }
    }
  }
};
</script>

<style>
.user-requests {
  padding: 20px;
}

.request-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
  text-align: center;
}

.request-table th,
.request-table td {
  border: 1px solid #ccc;
  padding: 10px;
}

.request-table th {
  background-color: #65eb85;
  color: rgb(1, 0, 0);
}

.request-table tr:nth-child(even) {
  background-color: #e0f7fa; /* Light blue color */
}

.request-table tr:nth-child(odd) {
  background-color: #ffffff; /* White color */
}

.cancel-button {
  background-color: #dc3545;
  color: white;
  border: none;
  padding: 5px 10px;
  cursor: pointer;
  border-radius: 3px;
}

.cancel-button:hover {
  background-color: #c82333;
}
</style>
