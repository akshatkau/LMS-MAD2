<template>
    <div class="admin-dashboard">
      <SectionManagement />
    </div>
  </template>
  
  <script>
  import SectionManagement from '../views/SectionManagement.vue'; // Adjusted the path
  
  export default {
    name: 'AdminDashboard',
    components: {
      SectionManagement
    }
    
}
  </script>
  
  <style>
  /* Add custom styles for Admin Dashboard if needed */
  </style>
  