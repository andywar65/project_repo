axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";

Vue.component('add-task', {
    delimiters: ["[[", "]]"],
    template: `
        <div>
            <div class="card border-dark p3" v-show="!isAdding" v-on:click="showAddForm">
                <div class="card-body text-dark">
                    <i class="fa fa-plus"></i> Add New Task
                </div>
            </div>

            <div class="card border-dark mb-3" v-show="isAdding">
                <div class="card-body text-dark">
                    <div class="form-group">
                        <label>Title</label>
                        <input type="text" class="form-control form-control-sm" v-model="title">
                    </div>
                    <div class="form-group">
                        <label>Description</label>
                        <input type="text" class="form-control form-control-sm" v-model="description">
                    </div>
                    <a href="#" class="card-link" v-on:click="createTask" ><i class="fa fa-check"></i></a>
                    <a href="#" class="card-link" v-on:click="hideForm" ><i class="fa fa-times"></i></a>

                </div>
            </div>
        </div>
    `,
    data() {
        return {
            isAdding: false,
            title: "",
            description: "",
        };
    },
    methods: {
        showAddForm() {
            this.isAdding = true;
        },
        hideForm() {
            this.isAdding = false;
        },
        createTask() {
            let url = '/tasks/api/';
            let data = {
                "title": this.title,
                "description": this.description,
            };
            axios
                .post(url, data)
                .then(response => {
                    this.isAdding = false;
                    this.$parent.fetchTasks();
                })
                .catch(error => {
                    console.log(error);
                });
        }
    },
});


Vue.component('task', {
    delimiters: ["[[", "]]"],
    props: {
        task: {
            type: Object,
            required: true
        }
    },
    template: `
        <div>
            <div class="card border-dark mb-3" v-show="!isEditing">
                <div class="card-body text-dark">
                    <h6 class="card-title">[[ task.title ]]</h6>
                    <p class="card-text">[[ task.description ]]</p>
                    <a href="#" class="card-link" v-on:click="deleteTask(task)"><i class="fa fa-trash-o"></i></a>
                    <a href="#" class="card-link" v-on:click="showForm" ><i class="fa fa-pencil-square-o"></i></a>
                    <a href="#" class="card-link" v-on:click="completeTask" v-show="canBeCompleted"><i class="fa fa-check"></i></a>

                </div>
            </div>

            <div class="card border-dark mb-3" v-show="isEditing">
                <div class="card-body text-dark">
                    <div class="form-group">
                        <label>Title</label>
                        <input type="text" class="form-control form-control-sm" v-model="task.title">
                    </div>
                    <div class="form-group">
                        <label>Description</label>
                        <input type="text" class="form-control form-control-sm" v-model="task.description">
                    </div>
                    <a href="#" class="card-link" v-on:click="hideForm" ><i class="fa fa-check"></i></a>

                </div>
            </div>
        </div>
    `,
    data() {
        return {
            isEditing: false,
        };
    },
    computed: {
        canBeCompleted() {
            return this.task.status !== 3;
        },
    },
    methods: {
        showForm() {
            this.isEditing = true;
        },
        hideForm() {
            let url = '/tasks/api/' + this.task.id + '/';
            let data = {
                "title": this.task.title,
                "description": this.task.description,
            };
            axios
                .put(url, data)
                .then(response => {
                    this.isEditing = false;
                })
                .catch(error => {
                    console.log(error);
                });
        },
        deleteTask(task) {
            this.$parent.deleteTaskFromBackend(task.id);
        },
        completeTask() {
            if (this.canBeCompleted) {
                let url = '/tasks/api/' + this.task.id + '/';
                let new_status = this.task.status + 1;
                axios
                    .patch(url, {"status": new_status})
                    .then(response => {
                        this.task.status = response.data.status;
                    })
                    .catch(error => {
                        console.log(error);
                    });
            }
        }
    },
});

let app = new Vue({
    delimiters: ["[[", "]]"],
    el: '#vue-app',
    data: {
        tasks: [],
        loading: true,
        errored: false,
    },
    computed: {
        backlog_tasks() {
            return this.tasks.filter(a => a.status === 0);
        },
        todo_tasks() {
            return this.tasks.filter(a => a.status === 1);
        },
        in_progress_tasks() {
            return this.tasks.filter(a => a.status === 2);
        },
        done_tasks() {
            return this.tasks.filter(a => a.status === 3);
        },
    },
    methods: {
        deleteTask(task_id) {
            const task = this.tasks.find((element)=> element.id === task_id);
            const taskIndex = this.tasks.indexOf(task);
            this.tasks.splice(taskIndex, 1);
        },
        deleteTaskFromBackend(task_id) {
            let url = '/tasks/api/' + task_id + '/delete/';
            axios
                .delete(url)
                .then(response => {
                    this.deleteTask(task_id)
                })
                .catch(error => {
                    console.log(error);
                });
        },
        fetchTasks() {
            axios
                .get('/tasks/api/')
                .then(response => {
                    this.tasks = response.data
                })
                .catch(error => {
                    console.log(error);
                    this.errored = true
                })
                .finally(() => this.loading = false)
        }
    },
    mounted() {
        this.fetchTasks();
    }
});
