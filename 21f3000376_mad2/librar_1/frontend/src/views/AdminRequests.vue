<template>
  <div class="admin-requests">
    <h1>User Book Requests</h1>

    

    <h3>Filter by Status:</h3>
    <div class="status-filter">
      <select v-model="selectedStatus" @change="filterRequests">
        <option value="">All</option>
        <option value="accepted">Accepted</option>
        <option value="pending">Pending</option>
        <option value="revoked">Revoked</option>
      </select>
    </div>

    <table v-if="filteredRequests.length > 0" class="request-table">
      <thead>
        <tr>
          <th>Username</th>
          <th>Book Name</th>
          <th>Author</th>
          <th>Status</th>
          <th>Return Date</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="request in filteredRequests" :key="request.id">
          <td>{{ request.user.username }}</td>
          <td>{{ request.book_name }}</td>
          <td>{{ request.book_author }}</td>
          <td>{{ request.status }}</td>
          <td>{{ request.return_date }}</td>
          <td>
            <button @click="updateRequestStatus(request.id, 'accepted')" v-if="request.status === 'pending'" class="accept-button">Accept</button>
            <button @click="updateRequestStatus(request.id, 'declined')" v-if="request.status === 'pending'" class="decline-button">Decline</button>
            <button @click="updateRequestStatus(request.id, 'revoked')" v-if="request.status === 'accepted'" class="revoke-button">Revoke</button>
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

export default {
  data() {
    return {
      requests: [],
      searchQuery: '',
      selectedStatus: '',
      filteredRequests: []
    };
  },
  created() {
    this.loadRequests();
  },
  methods: {
    async loadRequests() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/api/request/user/1');
        this.requests = response.data;
        this.filteredRequests = this.requests;
      } catch (error) {
        console.error(error);
      }
    },
    filterRequests() {
      this.filteredRequests = this.requests.filter(request => {
        const matchesStatus = this.selectedStatus ? request.status === this.selectedStatus : true;
        return matchesStatus;
      });
    },
    async updateRequestStatus(requestId, status) {
      try {
        await axios.put(`http://127.0.0.1:5000/api/request/${requestId}`, { status });
        this.loadRequests();
      } catch (error) {
        console.error(error);
      }
    }
  }
};
</script>

<style>
.admin-requests {
  padding: 20px;
}

.search-bar, .status-filter {
  margin-bottom: 20px;
  display: flex;
  justify-content: center;
}

.search-bar input, .status-filter select {
  padding: 10px;
  width: 30%;
  border-radius: 5px;
  border: 1px solid #ccc;
}

h3 {
  text-align: center;
  margin-top: 20px;
}

.request-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
  text-align: center;
}

.request-table th, .request-table td {
  border: 1px solid #ccc;
  padding: 10px;
}

.request-table th {
  background-color: #32a3e4;
  color: rgb(255, 255, 255);
}

.request-table tr:nth-child(even) {
  background-color: #e0f7fa; /* Light blue color */
}

.request-table tr:nth-child(odd) {
  background-color: #ffffff; /* White color */
}

.accept-button {
  background-color: #28a745;
  color: white;
  border: none;
  padding: 5px 10px;
  cursor: pointer;
  margin-right: 5px;
  border-radius: 3px;
}

.accept-button:hover {
  background-color: #218838;
}

.decline-button {
  background-color: #ffc107;
  color: white;
  border: none;
  padding: 5px 10px;
  cursor: pointer;
  margin-right: 5px;
  border-radius: 3px;
}

.decline-button:hover {
  background-color: #e0a800;
}

.revoke-button {
  background-color: #dc3545;
  color: white;
  border: none;
  padding: 5px 10px;
  cursor: pointer;
  margin-right: 5px;
  border-radius: 3px;
}

.revoke-button:hover {
  background-color: #c82333;
}
</style>
