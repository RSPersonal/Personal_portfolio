<template>
  <main>
    <div class="container-fluid">
      <div class="row">
        <h1>
          Placeholder
        </h1>
      </div>
    </div>
  </main>
</template>

<script>
export default {
  data() {
    return {
      visitorCount: 0
    }
  },
  methods: {
    async getVisitorCount() {
      try {
        const response = await this.axios.get('http://localhost:8000/api/v1/visitor-count');
        this.visitorCount = response.data['visitor_count'];
      } catch (error) {
        console.log(error);
        this.visitorCount = "API connection error"
      }
    },
    async getProfilePost() {
      try {
        const response = await this.axios.get('')
      } catch (error) {
        console.log(error)
      }
    }
  },
  created() {
    this.getVisitorCount();
  }
}
</script>
