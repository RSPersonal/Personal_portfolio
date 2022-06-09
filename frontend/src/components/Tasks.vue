<template>
  <div class="task_container">
    <div class="task_content">
      <h1>Tasks</h1>
      <ul class="task_list">
        <li v-for="task in tasks" :key="task.id">
          <h2>{{ task.title }}</h2>
          <p> {{ task.description }}</p>
          <button @click="toggleTask(task)">{{ task.completed ? 'Undo' : 'Complete' }}</button>
          <button @click="deleteTask(task)">Delete</button>
        </li>
      </ul>
      <div class="container">
        <div class="add_task">
          <form v-on:submit.prevent="submitForm">
            <div class="form-group">
              <label for="title">Title</label>
              <input type="text" class="form-control" id="title" v-model="title">
            </div>
            <div class="form-group">
              <label for="description">Description</label>
              <textarea class="form-control" id="description" v-model="description"></textarea>
            </div>
            <div class="form-group">
              <button type="submit">Add Task</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
export default {
  data() {
    return {
      tasks: [''],
      title: '',
      description: ''
    }
  },
  methods: {
    async getData() {
      try {
        const response = await this.$http.get('http://localhost:8000/api/v1/tasks/all')
        this.tasks = response.data
        console.log(this.tasks);
      } catch (error) {
        console.log(error)
      }
    },
    async submitForm() {
      try {
        const response = await this.$http.post('http://localhost:8000/api/v1/tasks/all', {
          title: this.title,
          description: this.description,
          completed: false
        })
        this.tasks.push(response.data)
        this.title = ''
        this.description = ''
      } catch (error) {
        console.log(error)
      }
    },
    async toggleTask(task) {
      try {
        const response = await this.$http.put(`http://localhost:8000/api/v1/task/${task.id}`, {
          completed: !task.completed,
          title: task.title,
          description: task.description,
        })
        let taskIndex = this.tasks.findIndex(t => t.id === task.id);
        this.tasks = this.tasks.map((task) => {
          if (this.tasks.findIndex(t => t.id === task.id) === taskIndex) {
            return response.data;
          }
        })
      } catch (error) {
        console.log(error)
      }
    },
     async deleteTask(task) {
      try {
        const response = await this.$http.delete('http://localhost:8000/api/v1/')
      } catch (error) {
        console.log(error)
      }
     }
  },
  created() {
    this.getData()
  }
}
</script>
