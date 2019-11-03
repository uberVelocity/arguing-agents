<template>
  <div>
    <div class="container">
      <h1>Rextractor</h1>
      <div class="tabs">
        <div class="row">
          <div class="col s12">
            <ul class="tabs">
              <li class="tab col s4"><a href="#test1">Some Data</a></li>
              <li class="tab col s4"><a href="#test2">Test 2</a></li>
              <li class="tab col s4"><a href="#test3">Test 3</a></li>
            </ul>
          </div>
          <div id="test1" class="col s12">{{someData}}</div>
          <div id="test2" class="col s12">Test 2</div>
          <div id="test3" class="col s12">Test 3</div>
        </div>
      </div>
      <div class="topic-select">
        <select v-model="topic">
          <option value="abortion">Abortion</option>
          <option value="gun control">Gun Control</option>
          <option value="school uniforms">School uniforms</option>
        </select>
        <button class="green waves-effect waves-light btn" @click="submitForm">Submit</button>
      </div>
      <div class="program-description">
        <p>
          Rextractor is an argument extraction tool that attempts to categorize arguments into pros and cons
          from natural language. It currently supports {{nTopics}} topics from which it is able to compile lists
          of pros and cons. The program compares its lists of pros and cons with pros and cons taken from www.procon.org.
        </p>
      </div>
    </div>
  </div>
</template>

<script>
import TabsComponent from "./TabsComponent";

import BackendService from "../services/BackendService";

export default {
  components: {
    TabsComponent
  },
  data() {
    return {
      nTopics: 3,
      topic: "",
      someData: "someDataBoy",
      debugResponse: "noResponse",
      ourPros: [],
      ourCons: [],
      proconPros: [],
      proconCons: [],
      nRequests: 0,
      nResponses: 0
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
      this.nRequests += 1;
      const response = await BackendService.processTopic(this.topic);
      this.debugResponse = response.data;
      this.nResponses += 1;

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

.header-list-pros {
  color: #4caf50;
  text-align: center;
  font-size: 30px;
}

.header-list-cons {
  color: #f44336;
  text-align: center;
  font-size: 30px;
}

.argument {
  text-align: justify;
}

.iter-arg {
  font-weight: bold;
}

select {
  display: block;
}
</style>