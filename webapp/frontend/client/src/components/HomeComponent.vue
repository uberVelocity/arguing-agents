<template>
  <div>
    <div class="container">
      <h1>Rextractor</h1>
      <div class="program-description">
        <p>
          Rextractor is an argument extraction tool that attempts to categorize arguments into pros and cons
          from natural language. It currently supports {{nTopics}} topics from which it is able to compile lists
          of pros and cons. The program compares its lists of pros and cons with pros and cons taken from www.procon.org.
        </p>
      </div>
      <div class="topic-select">
        <select>
          <option value="abort">Abortion</option>
          <option value="gun">Gun Control</option>
          <option value="uniform">School uniforms</option>
        </select>
        <button class="waves-effect waves-light btn" @click="submitForm">Submit</button>
      </div>
      <div class="row">
        <div class="lists-container">
          <div class="list col s6">
            <div class="row">
              <h4>Generated list</h4>
              <div class="col s6">
                <div
                  class="pros"
                  v-for="(pro, index) in ourPros"
                  v-bind:item="pro"
                  v-bind:index="index"
                  v-bind:key="pro.id"
                >{{pro.text}}</div>
              </div>
              <div class="col s6">
                <div
                  class="cons"
                  v-for="(con, index) in ourCons"
                  v-bind:item="con"
                  v-bind:index="index"
                  v-bind:key="con.id"
                >{{con.text}}</div>
              </div>
            </div>
          </div>
          <div class="list col s6">
            <div class="row">
              <h4>Procon list</h4>
              <div class="col s6">
                <div
                  class="proconPros"
                  v-for="(pro, index) in proconPros"
                  v-bind:item="pro"
                  v-bind:index="index"
                  v-bind:key="pro.id"
                >{{pro.text}}</div>
              </div>
              <div class="col s6">
                <div
                  class="proconCons"
                  v-for="(con, index) in proconCons"
                  v-bind:item="pro"
                  v-bind:index="index"
                  v-bind:key="con.id"
                >{{con.text}}</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      nTopics: 3,
      ourPros: [
        {
          id: 1,
          text: "Pro number 1"
        },
        {
          id: 2,
          text: "Pro number 2"
        }
      ],
      ourCons: [
        {
          id: 1,
          text: "Con number 1"
        },
        {
          id: 2,
          text: "Con number 2"
        }
      ],
      proconPros: [
        {
          id: 1,
          text: "Procon pro number 1"
        },
        {
          id: 2,
          text: "Procon pro number 2"
        }
      ],
      proconCons: [
        {
          id: 1,
          text: "Procon con number 1"
        },
        {
          id: 2,
          text: "Procon con number 2"
        }
      ]
    };
  },
  methods: {
    submitForm() {
      // Call the back-end to fetch the lists
    }
  }
};
</script>

<style scoped>
.program-description {
  text-align: justify;
}

.btn {
  margin: 100px 0px;
}

select {
  display: block;
}
</style>