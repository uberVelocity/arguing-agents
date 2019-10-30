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
      <h3> {{debugResponse}} </h3>
      <div class="topic-select">
        <select v-model="topic">
          <option value="abortion">Abortion</option>
          <option value="gun control">Gun Control</option>
          <option value="school uniforms">School uniforms</option>
        </select>
        <button class="green fwaves-effect waves-light btn" @click="submitForm">Submit</button>
      </div>
      <div class="row">
        <div class="lists-container">
          <div class="list col s6">
            <div class="row">
              <h4>Generated list</h4>
              <div class="col s6">
                <div
                  class="pros"
                >{{ourPros}}</div>
              </div>
              <div class="col s6">
                <div
                  class="cons"
                >{{ourCons}}</div>
              </div>
            </div>
          </div>
          <div class="list col s6">
            <div class="row">
              <h4>Procon list</h4>
              <div class="col s6">
                <div
                  class="proconPros"
                >{{proconPros}}</div>
              </div>
              <div class="col s6">
                <div
                  class="proconCons"
                >{{proconCons}}</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import BackendService from '../services/BackendService';

export default {
  data() {
    return {
      nTopics: 3,
      topic: '',
      debugResponse: 'noResponse',
      ourPros: [],
      ourCons: [],
      proconPros: [],
      proconCons: []
    };
  },
  // Relevance indicated from the OP getting his view changed
  // Just use the text that is typed by the OP and the text that changes their view and you interpret this as argumentative information
  // Extract this labeling and do something with it and comment on it: this is nice, not nice, needs NLP etc.
  // Compare the two sub projects to have a nice research: pursue more relevant research questions.
  // think of properties that you would like to ideally see in 'super good' argument mining (easy and difficult)
  // properties: {structure strategies, NLP strategies}
  // Hypothesis: Wordnes works nicely => actual results (why is it not good? etc...)
  // Pick well-cited papers on argument mining and write a bit on that research background and about what we are doing
  // Use Google Scholar to get papers on argument mining
  // Connect the properties to the literature!!!!!!!
  // Talk about the paper in a balanced way (not expected unless master thesis)-
 methods: {
    async submitForm() {
      const response = await BackendService.processTopic(this.topic);
      this.debugResponse = response.data;
      
      this.ourPros = response.data.prosReddit;
      this.ourCons = response.data.consReddit;
      this.proconPros = response.data.prosProcon;
      this.proconCons = response.data.consProcon;
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