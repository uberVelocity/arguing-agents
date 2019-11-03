<template>
  <div>
    <ul class="nav nav-tabs nav-justified">
      <li class="nav-item">
        <a
          class="nav-link"
          @click.prevent="setActive('per_argument')"
          :class="{ active: isActive('per_argument') }"
          href="#per_argument"
        >Home</a>
      </li>
      <li class="nav-item">
        <a
          class="nav-link"
          @click.prevent="setActive('graphs')"
          :class="{ active: isActive('graphs') }"
          href="#graphs"
        >Profile</a>
      </li>
      <li class="nav-item">
        <a
          class="nav-link"
          @click.prevent="setActive('top_comments')"
          :class="{ active: isActive('top_comments') }"
          href="#top_comments"
        >Contact</a>
      </li>
    </ul>
    <div class="tab-content py-3" id="myTabContent">
      <div
        class="tab-pane fade"
        :class="{ 'active show': isActive('per_argument') }"
        id="per_comment"
      >
        <TopCommentsPerArgumentComponent />
      </div>
      <div class="tab-pane fade" :class="{ 'active show': isActive('graphs') }" id="graphs">
        <GraphComponent />
      </div>
      <div
        class="tab-pane fade"
        :class="{ 'active show': isActive('top_comments') }"
        id="top_comments"
      >
        <HighestRatedComponent />
      </div>
    </div>
  </div>
</template>

<script>
import TopCommentsPerArgumentComponent from "./TopCommentsPerArgumentComponent";
import GraphComponent from "./GraphComponent";
import HighestRatedComponent from "./HighestRatedComments";

export default {
  components: {
    TopCommentsPerArgumentComponent,
    GraphComponent,
    HighestRatedComponent
  },
  data() {
    activeItem: "per_argument";
  },
  methods: {
    isActive(menuItem) {
      return this.activeItem === menuItem;
    },
    setActive(menuItem) {
      this.activeItem = menuItem;
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